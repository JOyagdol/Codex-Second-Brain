# 기억 위치 확인

아래 순서로 실제 존재하는 연결 설정을 읽는다. 임의의 URL/ID를 만들거나 자격증명을 찾지 않는다.

1. 현재 프로젝트 루트의 `config/notion.local.json` (프로젝트별 설정).
2. 이 스킬에 `references/memory-registry.local.json`이 제공되어 있으면 해당 개인 연결 정보.
3. Codex 환경에서는 `$CODEX_HOME/second-brain/notion.json`; CODEX_HOME이 없으면 `~/.codex/second-brain/notion.json`.

config의 `projects`에서 요청과 맞는 프로젝트를 선택한다. `default_project`는 모호할 때의 탐색 힌트이며 다른 과제를 그 프로젝트로 강제하지 않는다. `state_page`, `hub_page`, `sessions_data_source`, `decisions_data_source`, `literature_data_source`를 실제 fetch하고 스키마를 확인한다. 다른 환경에서 로컬 경로가 없으면 연결된 Notion에서 사용자가 지정한 허브를 찾는다. 연결 없이 자동 연동되었다고 말하지 않는다.

개인 연결 파일은 공개 저장소에 커밋하지 않는다. ZIP의 설정 파일은 주소만 포함하며 OAuth 인증이나 접근 권한을 대신하지 않는다.
