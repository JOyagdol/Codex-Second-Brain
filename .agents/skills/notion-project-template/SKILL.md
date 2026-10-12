---
name: notion-project-template
description: Create or adapt a Notion project hub with left navigation, a board-only right panel, seven connected source databases, filtered views, and a separate operating guide. Use for 노션 프로젝트 템플릿, ASIP 같은 프로젝트 관리 체계, Jira-style Notion boards, or updates to a hub built with this skill. Keep explicit user changes authoritative.
---

# Notion 프로젝트 템플릿

ASIP에서 확정한 문서 허브와 프로젝트 관리 구조를 다른 Notion 프로젝트에 재사용하라. 실제 Notion DB와 연결 View를 만들고, 기존 시스템에서는 요청받은 부분만 수정하라.

## 세션 간 맥락과 기록

연구·프로젝트 작업에 이 스킬을 적용할 때 [공통 기억 규칙](references/memory-protocol.md)을 먼저 읽는다. [기억 위치](references/memory-location.md)에서 해당 프로젝트의 최신 상태를 확인하고 중요한 변경·마무리 시 세션과 결정을 기록한다. 일반 설명·문구 수정에는 불필요한 전체 연구 검색을 하지 않는다. 같은 세션에서 이미 읽은 자료는 변경 가능성이 없으면 다시 읽지 않는다.

## 구성 원칙

- 메인 좌측은 메뉴 25%, 우측은 프로젝트 보드 75%로 구성하라. 파란 배경 제목과 파란 메뉴 링크를 사용하라.
- 우측에는 보드 제목과 하나의 Tasks Kanban만 두라. 오버뷰, 상태 안내, DB 설명, 사용법, 권장 흐름은 별도 운영 가이드로 옮겨라.
- 운영 가이드는 Documents의 Category=Guide, Area=General로 저장하고 좌측 프로젝트 관리 메뉴와 해당 하위 페이지에 mention 링크를 제공하라.
- DATABASE 아래 Projects, Tasks, Sprints, Requirements, Meetings, Documents, Resources를 원본으로 두라. 프론트엔드, 백엔드, Timeline, AI 문서, 자료 화면에는 원본의 연결 View를 사용하라.
- 내부 공식 문서는 Documents, 상시 서비스 링크·외부 참고·학습 자료는 Resources에 저장하라. Resources.Role로 Workspace / Reference / Learning을 구분하라.
- Jira 느낌은 Notion Board로 구현하라. 별도 Jira 서비스 연결을 추가하지 마라.
- 새 프로젝트에는 새로 생성하거나 명시적으로 재사용하기로 한 대상 DB의 ID만 사용하라. 출처 프로젝트의 업무나 개인 정보를 복사하지 마라.

## 요청 범위를 결정하라

1. 새 허브 요청에는 전체 구성을 적용하라. 프로젝트명은 대상 제목에서 추론하고 메뉴명은 에셋의 한국어·영문 표기를 그대로 사용하라. Dashboard, My Tasks, Sprint, Timeline도 번역 요청이 없으면 유지하라. 속성과 선택값은 에셋의 영문을 기본으로 사용하라.
2. 기존 허브 수정에는 현재 내용을 fetch하고 요청한 메뉴·뷰·속성만 조정하라. 전체 재생성으로 확대하지 마라.
3. 설계·설명만 요청하면 외부 쓰기를 하지 마라.
4. 대상 페이지가 불명확하면 제공된 맥락을 확인한 뒤 링크만 물어라. 담당자·일정·서비스 URL이 없으면 비워두라.
5. 사용자 변경이 기본값보다 우선한다. 변경된 속성·상태·메뉴에 연결된 필터·수식·가이드도 일관되게 조정하라.

## 자료를 선택하라

| 작업 | 자료 |
| --- | --- |
| 새 허브 또는 DB 수정 | [DB 설계](assets/database-blueprint.json), [Notion 실행 절차](references/notion-workflow.md) |
| 메뉴·레이아웃 | [페이지 설계](assets/page-blueprint.json), [메인 레이아웃](assets/hub.md) |
| Kanban·Timeline·자료 화면 | [29개 연결 뷰](assets/views.json) |
| 기본 문서·회의록·운영 가이드 | [8개 문서 양식](assets/starter-documents.json) |

에셋은 Notion에 작성할 콘텐츠와 요청 구성 재료다. 원본 파일을 편집하지 말고 메모리나 작업 사본에서 조정하라. 새 허브의 기본 세트는 메뉴 페이지 22개, 원본 DB 7개, 연결 뷰 29개, Documents 항목 7개와 회의록 복제 양식 1개다.

## 새 허브를 구축하라

1. Notion fetch·create_pages·create_database·update_data_source·create_view·update_page 기능과 현재 스키마를 확인하라. 최신 enhanced-markdown과 view DSL 문서를 읽어라.
2. 대상 페이지를 fetch해 본문·자식 페이지·DB·아이콘을 확인하라. 기존 내용을 보존하면서 구조를 추가하고 충돌하는 대상만 확인하라.
3. 페이지 에셋의 parent 순서로 메뉴를 생성하고 반환 ID를 기록하라. 처음에는 initial_content만 써서 아직 없는 자식이나 연결 뷰를 참조하지 마라.
4. DATABASE 아래 7개 기본 스키마를 만들거나 같은 대상의 기존 DB를 재사용하라. 각 DB를 fetch해 data_source ID와 실제 속성명을 확인하라.
5. 17개 Relation 선언을 순서대로 적용하라. DUAL이 만든 반대 속성을 다시 추가하지 마라. Tasks.Parent Task는 단방향 자기 Relation이다.
6. Tasks.Completed 수식을 만든 뒤 13개 Rollup을 적용하라. Project·Sprint Progress는 연결 Tasks의 Completed에 대한 percent_checked다. 수동 진행률을 별도로 만들지 마라.
7. Projects 레코드를 생성하고 record.project를 기록하라. 신규 기본 상태는 Planning이며, 실제 진행 맥락이 있으면 Active 등을 선택하라. 날짜를 추측하지 마라.
8. Documents와 Meetings에 기본 문서를 작성하라. 새 Project에 연결하고 문서는 Draft로 두라. 미확정 정책을 확정 사실로 제시하지 마라.
9. 뷰 에셋에 따라 각 페이지에 연결 View를 생성하라. 새 프로젝트 레코드로 필터하고 연결 DB 블록 ID와 saved view ID를 별도로 기록하라.
10. 페이지를 다시 fetch하라. 실제 자식 페이지·연결 DB 블록과 가이드 mention을 보존하여 final_content를 반영하라. 메인은 hub.md에 새 ID를 채워 메뉴와 보드만 배치하라.
11. 아래 검증을 완료하고 실제 허브 링크를 전달하라. 미입력 담당자·일정·주소는 필요할 때 짧게 안내하라.

## 기본 문서를 적용하라

- 시스템 아키텍처, API 및 데이터베이스 가이드, QA 및 테스트 체계, 버전 관리 체계, 배포 체계, 요구사항 관리 가이드, 프로젝트 운영 가이드를 Documents에 생성하라.
- AI Prompt / AI Skill / Business 등의 분류와 필터를 제공하되 사용자가 내용을 주지 않았다면 가짜 프로젝트 문서를 채우지 마라.
- 참고용 사업계획서·경영 공부 자료는 Resources의 Business 영역, 직접 작성한 사업계획서는 Documents의 Business 분류로 관리하라.
- 회의록 양식은 Meetings.Type=Template인 일반 DB 행이다. 실제 native template 생성이 확인되지 않았다면 ‘복제하여 사용’이라고 안내하라.
- 실제 Task·Requirement·Sprint·Meeting 기록은 제공된 내용만 작성하라. 빈 보드를 채우기 위해 가짜 업무·일정·회의를 만들지 마라.
- 초안의 브랜치·CI/CD·QA 규칙은 팀 합의용이다. 실제 서비스 설정 변경이나 배포를 실행하지 마라.

## 검증하라

- 기본 원본 DB가 7개이며 메뉴별 독립 복제 DB가 없는지 확인하라.
- 메인 우측에는 제목과 Tasks 연결 보드만, 운영 설명은 Guide에 있는지 확인하라.
- 연결 View의 data_source와 Project가 이번 대상인지 확인하라. My Tasks는 현재 사용자 me로 설정하라.
- Formula·Rollup 정의와 역방향 Relation을 확인하라. 빈 DB에서 검증용 가짜 업무를 만들지 마라.
- saved view fetch로 필터·정렬·표시 속성·Timeline 날짜를 확인하라. 카드 이동은 Status를 바꾸며 날짜를 자동 변경하지 않는다.
- 가이드·기본 문서의 Project 연결, 회의 양식 분리, 자식 블록 보존을 확인하라.
- 재실행 시 기록한 ID와 현재 본문을 비교해 누락만 채우고 중복을 만들지 마라.
- 접근·쓰기 제한이 있으면 완료된 부분과 막힌 동작을 구분해 보고하라. 확인된 범위만 완료로 안내하라.
