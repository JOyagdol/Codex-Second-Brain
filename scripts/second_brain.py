#!/usr/bin/env python3
"""Portable, standard-library-only skill installer and Git sync helper (Python 3.10+)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'https://github.com/JOyagdol/Codex-Second-Brain.git'
BEGIN = '<!-- research-second-brain:start -->'
END = '<!-- research-second-brain:end -->'
PUBLIC_TOP = {'.agents', '.codex', '.github', 'config', 'docs', 'scripts', 'tests', 'templates'}
PUBLIC_FILES = {'AGENTS.md', 'README.md', 'START_HERE.md', 'VERSION', '.gitignore', '.gitattributes'}
SENSITIVE = [
    re.compile(r'(?:https?://(?:www\.|app\.)?notion\.(?:so|com)/[^\s)<>]*[a-f0-9]{32}|collection://[a-f0-9]{8}-[a-f0-9-]{27})'),
    re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|ntn_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,})\b'),
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
]

def fail(message):
    raise RuntimeError(message)

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.second-brain-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)

def preflight_shape(path):
    """Reject predictable filesystem conflicts before writing any installation file."""
    if path.is_symlink() or any(p.is_symlink() for p in path.parents):
        fail(f'Symlink destination/ancestor; install not changed: {path}')
    if path.exists() and not path.is_file():
        fail(f'Expected a file; install not changed: {path}')
    for parent in path.parents:
        if parent.exists() and not parent.is_dir():
            fail(f'Parent is not a directory; install not changed: {parent}')

def private_path(rel):
    return (any(x in {'.git', 'private', 'dist', '.state', '__pycache__', 'archive'} for x in rel.parts)
            or rel.name.endswith(('.local.json', '.pyc', '.zip')) or rel.name.startswith('.env'))

def public_files(root=ROOT):
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if private_path(rel):
            continue
        if p.is_file() and (rel.as_posix() in PUBLIC_FILES or rel.parts[0] in PUBLIC_TOP):
            if p.is_symlink():
                fail(f'Symlink not allowed in distribution: {rel}')
            yield p

def validate(root=ROOT):
    manifest = read_json(root/'config/skills.json')
    names = manifest['skills']
    if len(names) != len(set(names)):
        fail('Duplicate skill names')
    standard = None
    for name in names:
        folder = root/'.agents/skills'/name
        text = (folder/'SKILL.md').read_text(encoding='utf-8')
        m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        if not m or not re.search(r'^name: '+re.escape(name)+r'\s*$', m[1], re.M):
            fail(f'Invalid name/frontmatter: {name}')
        if not re.search(r'^description: .+', m[1], re.M):
            fail(f'Missing description: {name}')
        for p in folder.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
                if ':' not in target and not target.startswith('#'):
                    q = (p.parent/target.split('#')[0]).resolve()
                    if not q.is_relative_to(folder.resolve()) or not q.exists():
                        fail(f'Broken/local-outside link: {p.relative_to(root)} -> {target}')
        protocol = (folder/'references/memory-protocol.md').read_bytes()
        if standard is None:
            standard = protocol
        elif standard != protocol:
            fail('Common memory protocol differs across skills')
        if not (folder/'agents/openai.yaml').exists():
            fail(f'Missing agent metadata: {name}')
    print(f'Validated {len(names)} skills and their local references')

def audit(root=ROOT):
    files = list(public_files(root))
    for p in files:
        text = p.read_text(encoding='utf-8')
        if any(rule.search(text) for rule in SENSITIVE):
            fail(f'Private identifier or credential pattern in {p.relative_to(root)}')
    print(f'Audited {len(files)} public files (pattern check, not a confidentiality guarantee)')

def codex_home():
    return Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex'))).expanduser().resolve()

def install(scope='user', target=None, root=ROOT, home=None, codex=None):
    validate(root)
    base = Path(target).expanduser().resolve() if target else (Path(home) if home else Path.home())
    if scope == 'project' and target is None:
        fail('--target is required for project installation')
    ch = Path(codex) if codex else codex_home()
    skills_dir = base/'.agents/skills'
    control = (ch/'second-brain') if scope == 'user' else (base/'.second-brain')
    state_path = control/'installed.json'
    previous = read_json(state_path).get('files', {}) if state_path.exists() else {}
    planned = {}
    source_base = root/'.agents/skills'
    for name in read_json(root/'config/skills.json')['skills']:
        for p in sorted((source_base/name).rglob('*')):
            if p.is_file() and not private_path(p.relative_to(root)):
                planned[skills_dir/p.relative_to(source_base)] = p.read_bytes()
    config = root/'config/notion.local.json'
    if config.exists():
        read_json(config)  # fail before modifying any installed files
        dest_config = ch/'second-brain/notion.json' if scope == 'user' else base/'config/notion.local.json'
        planned[dest_config] = config.read_bytes()
    guidance = (ch/'AGENTS.md') if scope == 'user' else (base/'AGENTS.md')
    current = guidance.read_text(encoding='utf-8') if guidance.exists() else ''
    block = (BEGIN+'\n연구 작업에만 Research Second Brain을 적용한다.\n'
             'Read the relevant installed SKILL.md and references/memory-protocol.md.\n'
             'Read config/notion.local.json in the project, or $CODEX_HOME/second-brain/notion.json '
             '(default ~/.codex/second-brain/notion.json), then fetch the matching Notion Research State.\n'
             'Record meaningful checkpoints and handoffs; keep research state out of public Git.\n'
             'Do not claim remote sync or Notion writes without checking their result.\n'+END)
    if (BEGIN in current) != (END in current) or current.count(BEGIN)>1 or current.count(END)>1:
        fail('Malformed managed AGENTS block; preserve file and resolve manually')
    if BEGIN in current:
        old_block = current[current.index(BEGIN):current.index(END)+len(END)]
        prior_block = read_json(state_path).get('agents_block_sha256') if state_path.exists() else None
        if old_block != block and digest(old_block.encode()) != prior_block:
            fail('Managed AGENTS block was edited locally; merge before reinstalling')
        next_text = current.replace(old_block, block)
    else:
        next_text = current.rstrip()+'\n\n'+block+'\n'
    backup = control/'backups'/('AGENTS-'+digest(current.encode())[:12]+'.md') if guidance.exists() and current != next_text else None
    ignore_path = base/'.gitignore' if scope == 'project' else None
    ignore_content = None
    if ignore_path is not None:
        old_ignore = ignore_path.read_text(encoding='utf-8') if ignore_path.exists() else ''
        rules = ['/.second-brain/', '/config/notion.local.json', '/private/pending/']
        missing = [rule for rule in rules if rule not in old_ignore.splitlines()]
        if missing:
            ignore_content = (old_ignore.rstrip()+'\n\n# Research Second Brain personal files\n'+'\n'.join(missing)+'\n').encode()
    for path in [*planned, guidance, state_path, *([backup] if backup else []), *([ignore_path] if ignore_path else [])]:
        preflight_shape(path)
    # Preflight all file conflicts before any write. Identical files can be adopted safely.
    for path, data in planned.items():
        if path.is_symlink():
            fail(f'Destination is a symlink; install not changed: {path}')
        if path.exists() and path.read_bytes() != data:
            if digest(path.read_bytes()) != previous.get(str(path)):
                fail(f'Local/unmanaged change; install not changed: {path}')
    # Exclude personal files after all preflight checks and before creating them.
    if ignore_content is not None:
        write_atomic(ignore_path, ignore_content)
    for path, data in planned.items():
        if not path.exists() or path.read_bytes() != data:
            write_atomic(path, data)
    if current != next_text:
        if backup:
            if not backup.exists():
                write_atomic(backup, current.encode())
        write_atomic(guidance, next_text.encode())
    state = {'version':(root/'VERSION').read_text().strip(), 'source':str(root),
             'files':{str(p):digest(data) for p,data in planned.items()},
             'agents_block_sha256':digest(block.encode())}
    write_atomic(state_path, (json.dumps(state,indent=2)+'\n').encode())
    print(f'Installed {len(read_json(root/"config/skills.json")["skills"])} skills into {skills_dir}')
    print('Preserved unrelated files. Notion OAuth and PC runtime loading are separate checks.')

def git(*args, root=ROOT):
    result = subprocess.run(['git','-C',str(root),*args],text=True,capture_output=True)
    if result.returncode:
        fail(result.stderr.strip() or result.stdout.strip() or 'git command failed')
    return result.stdout.strip()

def require_repo(root=ROOT):
    if not (root/'.git').exists():
        fail('This is a ZIP copy. Clone the GitHub repository, copy config/notion.local.json into it, then run install/sync there.')
    if git('rev-parse','--show-toplevel',root=root) != str(root.resolve()):
        fail('Not at the configured repository root')
    url = git('remote','get-url','origin',root=root).rstrip('/')
    if url.removesuffix('.git') not in {REPOSITORY.removesuffix('.git'),'git@github.com:JOyagdol/Codex-Second-Brain'}:
        fail('Unexpected origin; refusing automatic synchronization')

def sync(scope='user', target=None):
    require_repo()
    if git('status','--porcelain'):
        fail('Working tree has changes; commit or merge them before sync. No reset/stash was performed.')
    branch = git('branch','--show-current')
    if not branch:
        fail('Detached HEAD: choose an intended branch first')
    git('pull','--ff-only','origin',branch)
    install(scope,target)

def publish(message, paths):
    require_repo()
    validate(); audit()
    if git('diff','--cached','--name-only'):
        fail('Index already contains staged work; preserve it and publish explicitly after review')
    allowed = {p.relative_to(ROOT).as_posix() for p in public_files()}
    for path in paths:
        rel = Path(path)
        if rel.is_absolute() or '..' in rel.parts or rel.as_posix() not in allowed:
            fail(f'Explicit existing public file required: {path}')
    branch = git('branch','--show-current')
    if not branch:
        fail('Detached HEAD')
    git('fetch','origin',branch)
    remote = git('rev-parse','FETCH_HEAD')
    if git('merge-base','HEAD',remote) != remote:
        fail('Remote advanced/diverged. Read and merge first; no force push performed.')
    git('add','--',*paths)
    if git('diff','--cached','--name-only'):
        git('commit','-m',message)
    git('push','origin',branch)
    print('Pushed',git('rev-parse','HEAD'))
    print('Update ChatGPT installed skills through that host, then record the commit in Notion.')

def package(output, include_personal=False, root=ROOT):
    validate(root); audit(root)
    files = list(public_files(root))
    if include_personal:
        config = root/'config/notion.local.json'
        if not config.exists():
            fail('Personal package requested without config/notion.local.json')
        cfg=read_json(config)
        if not cfg.get('hub_page'):
            fail('Personal config has no hub_page')
        files.append(config)
        private = root/'private'
        if private.exists():
            files.extend(p for p in sorted(private.rglob('*')) if p.is_file() and '__pycache__' not in p.parts)
    out=Path(output).expanduser().resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    if out.is_relative_to(root/'.agents') or out in files:
        fail('Invalid output location')
    hashes={p.relative_to(root).as_posix():digest(p.read_bytes()) for p in files}
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p,'Codex-Second-Brain/'+p.relative_to(root).as_posix())
        z.writestr('Codex-Second-Brain/PACKAGE_MANIFEST.json',json.dumps({'version':(root/'VERSION').read_text().strip(),'personal':include_personal,'files':hashes},indent=2))
    print(f'Created {out} ({len(files)} files; personal={include_personal})')

def doctor():
    validate()
    print('Python:',sys.version.split()[0])
    print('Git:',shutil.which('git') or 'not found')
    print('Codex:',shutil.which('codex') or 'not found')
    print('Personal config:', 'present' if (ROOT/'config/notion.local.json').exists() else 'not in this folder')
    print('Next: codex mcp list; authenticate Notion if necessary, then fetch the configured state in Codex.')
    print('Doctor does not claim OAuth, connectivity, or agent runtime readiness.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ['validate','audit','doctor']:
        sub.add_parser(name)
    for name in ['install','sync']:
        p=sub.add_parser(name);p.add_argument('--scope',choices=['user','project'],default='user');p.add_argument('--target')
    p=sub.add_parser('publish');p.add_argument('--message',required=True);p.add_argument('--paths',nargs='+',required=True)
    p=sub.add_parser('package');p.add_argument('--output',required=True);p.add_argument('--include-personal',action='store_true')
    a=parser.parse_args()
    if a.command=='validate':validate()
    elif a.command=='audit':audit()
    elif a.command=='doctor':doctor()
    elif a.command=='install':install(a.scope,a.target)
    elif a.command=='sync':sync(a.scope,a.target)
    elif a.command=='publish':publish(a.message,a.paths)
    elif a.command=='package':package(a.output,a.include_personal)

if __name__=='__main__':
    try:
        main()
    except (RuntimeError,OSError,ValueError) as exc:
        print('ERROR:',exc,file=sys.stderr);sys.exit(1)
