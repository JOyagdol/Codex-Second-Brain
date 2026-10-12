# Codex로 이전하기

이 폴더를 Codex에서 열고 다음 요청을 전달하세요.

> 이 폴더의 README.md와 AGENTS.md를 읽고 Research Second Brain을 설치해줘. Python과 Codex 환경을 확인하고 scripts/second_brain.py의 doctor와 validate를 실행한 뒤 사용자 범위로 설치해줘. 기존 스킬이나 AGENTS.md와 충돌하면 덮어쓰지 말고 차이를 확인해줘. 개인 config/notion.local.json은 공개 Git에 넣지 마. Notion MCP가 없으면 연결 설정을 하고 OAuth는 내가 진행할 수 있게 안내해줘. 연결되면 world-graph-aei의 Research State와 관련 기록을 읽고 실제로 이어받은 맥락을 짧게 요약해줘. 마지막으로 설치 경로·읽은 상태·미완료 항목을 알려줘.

## 개인 ZIP과 공개 저장소

- 개인 ZIP: 공개 스킬 + 개인 Notion 연결 주소 + 기존 스킬의 이관 백업. 인증 토큰은 없습니다.
- GitHub: 공개 가능한 스킬·운영 규칙·도구만 있습니다.
- `.git`은 ZIP에 포함되지 않습니다. 지속 동기화는 README의 clone 방식으로 전환하세요.
- ZIP을 풀었다는 사실만으로 설치나 OAuth가 완료되지 않습니다. 설치 스크립트 성공과 Notion fetch를 확인하세요.
- `private/imported-skills/`는 이관 전 백업입니다. 현재 스킬로 중복 설치하지 마세요.

설치 후 예시 요청: `$world-graph-research-partner 지금 Research State를 읽고, 마지막 작업에서 이어서 진행하자.`
