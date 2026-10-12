# Notion 기억 구조

개인 URL/ID는 `config/notion.local.json`에만 기록합니다. 인증정보는 Codex/Notion OAuth 저장소가 관리합니다. 공개 예시 설정에는 null을 사용합니다.

## 페이지

Research Second Brain 허브에 프로젝트별 Research State, AI Sessions DB, Decisions DB, 이관 기록을 연결합니다. 기존 연구 허브와 Literature DB를 재사용하며 옮기거나 복제하지 않습니다.

Research State는 짧게 유지합니다: Project ID, version, 업데이트 시각, 각 사실의 출처·확인 시점, 목표, 확정 결정, 후보 가설, 미해결, 다음 작업, 근거 링크. 보관일과 검증일을 구분합니다.

## AI Sessions

| 속성 | 형식 |
| --- | --- |
| Session | 제목 |
| Session ID | 충돌하지 않는 텍스트 ID |
| Project | 프로젝트 ID |
| Date | 날짜/시각 |
| Agent | ChatGPT / Codex / Other |
| Status | In progress / Completed / Blocked / Pending sync |
| Skills | 적용한 스킬 |
| Commit | 실제 commit, 없으면 비움 |
| Next Action | 다음에 시작할 작업 |

상세 내용은 row 본문에 기록합니다. 같은 ID로 재실행한 작업은 기존 항목을 갱신하고 다른 세션의 기록을 덮어쓰지 않습니다.

## Decisions

| 속성 | 형식 |
| --- | --- |
| Decision / Decision ID | 제목 / 고유 ID |
| Project / Date | 프로젝트 / 결정일 |
| Status | Proposed / Accepted / Deferred / Rejected / Superseded |
| Basis | User decision / Verified evidence / AI proposal / Imported record |
| Evidence | 근거·채택 주체 |
| Reversal Condition | 판단이 바뀔 조건 |
| Supersedes | 이전 결정 ID |

실제 쓰기 전 DB를 fetch해 현재 속성명을 사용합니다. 도구에서 날짜가 분리 키를 요구하면 해당 도구 스키마를 따릅니다. 새 스키마를 임의로 덧붙이지 않습니다.

Notion 쓰기는 MCP를 제공받은 AI가 수행합니다. 이 저장소는 토큰을 수집하거나 자체 Notion SDK/API 동기화를 실행하지 않습니다.
