# Codex Second Brain

이 저장소는 스킬과 운영 규칙의 원본이다. 연구 구현·실험 저장소가 아니다.

## 작업 시작

- 연구 작업은 `docs/MEMORY_PROTOCOL.md`와 요청에 해당하는 `.agents/skills/<name>/SKILL.md`를 읽고 시작한다.
- `config/notion.local.json` 또는 호스트의 개인 연결 설정으로 Notion 현재 상태를 읽는다. 없는 정보를 만들어내지 않는다. 오프라인에서는 미확인을 알리고 `private/pending/`에 인계 기록을 보존한다.
- Git 상태와 현재 branch를 먼저 확인한다. 원격 반영 전 최신 head와 사용자 변경을 확인한다.

## 수정·저장

- 스킬 name을 유지한다. 공통 기억 문서를 바꾸면 모든 스킬의 `references/memory-protocol.md`도 같은 내용으로 유지한다.
- 중요한 연구 결정과 결과는 Notion에, 반복 사용할 작업 규칙만 스킬에 기록한다.
- `python scripts/second_brain.py validate` 및 변경에 해당하는 테스트를 실행한다. 공개 반영 전 `python scripts/second_brain.py audit`를 실행한다.
- 작업한 경로만 명시적으로 stage한다. `git add .`, force push, 사용자 수정 덮어쓰기를 하지 않는다. 보호 브랜치는 PR로 진행한다.
- 사용자 요청 범위의 commit/push를 수행한다. 인증이나 정책이 막으면 제한을 알리고 로컬 결과를 보존한다.
- 공개 Git에는 `private/`, `*.local.json`, Notion 개인 URL/ID, 미공개 연구·특허, 인증정보를 넣지 않는다. 삭제된 민감 정보도 이전 commit에 남는다는 점을 고려하여 commit 전에 점검한다.
- 완료 시 commit, 실제 검증, Notion 저장, ChatGPT 설치 반영, Codex PC 적용을 각각 보고한다. 미실행을 완료로 쓰지 않는다.

## 설치와 실행

프로젝트 내부에서는 `.agents/skills`가 직접 발견된다. 다른 프로젝트에서도 쓰려면 README의 사용자 설치를 수행한다. 설치 도구는 기존 파일을 보존하며 사용자가 수정한 관리 파일과 충돌하면 중단한다. 호스트 연결·권한이나 승인 정책을 우회하지 않는다.
