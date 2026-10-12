import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('second_brain',ROOT/'scripts/second_brain.py')
sb=importlib.util.module_from_spec(spec);spec.loader.exec_module(sb)

class InstallSafety(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        self.source=self.base/'source';shutil.copytree(ROOT,self.source,ignore=shutil.ignore_patterns('.git','private','__pycache__'))
        self.home=self.base/'home';self.codex=self.base/'codex'
        self.name=json.loads((self.source/'config/skills.json').read_text())['skills'][0]

    def tearDown(self):self.tmp.cleanup()

    def install(self):
        with contextlib.redirect_stdout(io.StringIO()):sb.install(root=self.source,home=self.home,codex=self.codex)

    def test_idempotence_preserves_existing_guidance_and_unrelated_skills(self):
        self.codex.mkdir();(self.codex/'AGENTS.md').write_text('My existing instructions\n')
        other=self.home/'.agents/skills/unrelated/SKILL.md';other.parent.mkdir(parents=True);other.write_text('untouched')
        self.install();before=(self.codex/'AGENTS.md').read_bytes();self.install()
        self.assertEqual(before,(self.codex/'AGENTS.md').read_bytes())
        self.assertIn(b'My existing instructions',before)
        self.assertEqual(other.read_text(),'untouched')
        self.assertEqual(before.decode().count(sb.BEGIN),1)

    def test_unmanaged_collision_aborts_before_writing(self):
        target=self.home/'.agents/skills'/self.name/'SKILL.md';target.parent.mkdir(parents=True);target.write_text('my custom skill')
        with self.assertRaises(RuntimeError):self.install()
        self.assertEqual(target.read_text(),'my custom skill')
        self.assertFalse((self.codex/'AGENTS.md').exists())
        self.assertEqual(len(list((self.home/'.agents/skills').iterdir())),1)

    def test_managed_local_edit_is_not_overwritten(self):
        self.install();target=self.home/'.agents/skills'/self.name/'SKILL.md'
        target.write_text(target.read_text()+'\nUser local addition\n')
        with self.assertRaises(RuntimeError):self.install()
        self.assertIn('User local addition',target.read_text())

    def test_managed_source_update_and_outside_guidance_edit(self):
        self.install();source=self.source/'.agents/skills'/self.name/'SKILL.md';source.write_text(source.read_text()+'\nNew workflow rule\n')
        g=self.codex/'AGENTS.md';g.write_text('My new instruction\n'+g.read_text())
        self.install()
        self.assertIn('New workflow rule',(self.home/'.agents/skills'/self.name/'SKILL.md').read_text())
        self.assertTrue(g.read_text().startswith('My new instruction'))

    def test_package_excludes_private_by_default(self):
        cfg=self.source/'config/notion.local.json';cfg.write_text(json.dumps({'hub_page':'personal-placeholder'}))
        secret=self.source/'private/pending/item.md';secret.parent.mkdir(parents=True);secret.write_text('Unpublished research')
        pub=self.base/'public.zip';personal=self.base/'personal.zip'
        with contextlib.redirect_stdout(io.StringIO()):
            sb.package(pub,root=self.source);sb.package(personal,True,root=self.source)
        with zipfile.ZipFile(pub) as z:
            self.assertNotIn('Codex-Second-Brain/config/notion.local.json',z.namelist())
            self.assertFalse(any('/private/' in n for n in z.namelist()))
        with zipfile.ZipFile(personal) as z:
            self.assertIn('Codex-Second-Brain/config/notion.local.json',z.namelist())
            self.assertEqual(z.read('Codex-Second-Brain/private/pending/item.md'),b'Unpublished research')

    def test_audit_rejects_private_notion_identifier(self):
        url='https://www.'+'notion.so/'+'a'*32
        (self.source/'docs/leaked.md').write_text(url)
        with self.assertRaises(RuntimeError):sb.audit(self.source)

    def test_guidance_symlink_is_preserved(self):
        self.codex.mkdir();original=self.base/'original.md';original.write_text('linked guidance')
        guide=self.codex/'AGENTS.md'
        try:guide.symlink_to(original)
        except OSError:self.skipTest('Symlinks unavailable')
        with self.assertRaises(RuntimeError):self.install()
        self.assertTrue(guide.is_symlink())
        self.assertFalse((self.home/'.agents').exists())

    def test_backup_parent_conflict_aborts_before_writes(self):
        (self.codex/'second-brain').mkdir(parents=True)
        (self.codex/'AGENTS.md').write_text('existing')
        (self.codex/'second-brain/backups').write_text('not a directory')
        with self.assertRaises(RuntimeError):self.install()
        self.assertFalse((self.home/'.agents').exists())
        self.assertEqual((self.codex/'AGENTS.md').read_text(),'existing')

    def test_project_private_files_ignored_before_install(self):
        if not shutil.which('git'):self.skipTest('git unavailable')
        target=self.base/'project';target.mkdir()
        subprocess.run(['git','init',str(target)],check=True,capture_output=True)
        (self.source/'config/notion.local.json').write_text(json.dumps({'hub_page':'personal-placeholder'}))
        with contextlib.redirect_stdout(io.StringIO()):sb.install('project',target,root=self.source,home=self.home,codex=self.codex)
        result=subprocess.run(['git','-C',str(target),'check-ignore','config/notion.local.json','.second-brain/installed.json'],capture_output=True,text=True,check=True)
        self.assertEqual(len(result.stdout.splitlines()),2)

    def test_project_conflict_preserves_ignore_file(self):
        target=self.base/'project';p=target/'.agents/skills'/self.name/'SKILL.md'
        p.parent.mkdir(parents=True);p.write_text('local skill')
        with self.assertRaises(RuntimeError):sb.install('project',target,root=self.source,home=self.home,codex=self.codex)
        self.assertFalse((target/'.gitignore').exists())

if __name__=='__main__':unittest.main()
