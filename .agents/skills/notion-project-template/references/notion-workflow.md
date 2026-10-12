# Notion 실행 절차

## 목차
- 치환 키와 생성 순서
- 도구 사용
- 관계와 진행률
- 연결 뷰
- 페이지 편집과 재실행
- 검증과 중단 조건

## 치환 키와 생성 순서

입력과 반환 ID를 다음 키로 기록하라. 작업 메모리 또는 scratch JSON에 생성 직후 체크포인트를 갱신하라. 스킬 자체에 실행 ID를 저장하지 마라.

| 키 | 값 |
| --- | --- |
| `{{project_name}}` | 확인한 프로젝트명 |
| `{{project_status}}` | 실제 상태 또는 신규 기본 Planning |
| `{{page.root}}` | 이번 허브 대상 URL |
| `{{page.KEY}}` | page-blueprint의 key에 해당하는 메뉴 URL |
| `{{db.DBNAME}}` | 7개 원본 데이터베이스 블록 URL |
| `{{ds.DBNAME}}` | fetch의 data_source UUID; collection:// 접두사 제외 |
| `{{record.project}}` | Projects 안의 프로젝트 레코드 URL |
| `{{record.guide}}` | Documents 안의 운영 가이드 URL |
| `{{linked.PAGE.INDEX}}` | views.json key에 해당하는 연결 DB 블록 URL |

page.project는 메뉴이고 record.project는 DB 레코드다. ds.Tasks는 원본 컬렉션, db.Tasks는 원본 DB 블록, linked.root.0는 메인의 연결 DB 블록이다. saved view의 view:// UUID를 레이아웃 블록 URL로 쓰지 마라.

각 문자열의 치환 키를 실제 값으로 바꾸고 Markdown·XML·SQL·view DSL 문맥에 맞게 escape하라. 미치환 키가 남으면 해당 쓰기를 보내지 마라. 모든 대상 ID는 이번 작업의 API 응답 또는 확인된 재사용 대상에서 가져오라.

페이지 본문에 순환 참조가 있으므로 먼저 ID를 만든 뒤 링크를 배치하라. final_content를 생성 첫 단계에서 사용하지 마라. hub.md의 직접 자식 page 태그는 계층을 유지하고 하위 메뉴와 운영 가이드는 mention으로 연결한다.

## 도구 사용

현재 도구 스키마는 오래된 예보다 우선한다. Notion plugin을 사용하고 연결 실패를 브라우저나 별도 토큰 탐색으로 우회하지 마라. 초기 create_database 응답만으로 행 생성을 진행하지 말고 fetch로 실제 schema와 collection://를 확인하라.

- 메뉴 생성: create_pages의 parent.page_id와 pages 배열.
- DB 행 생성: parent.data_source_id. ID 또는 URL 예약명은 userDefined:ID / userDefined:URL 키를 사용하라.
- 원본 DB 생성: DATABASE 메뉴를 parent로 삼고 에셋의 schema를 전달하라.
- 관계 생성: update_data_source로 한 방향씩 선언하라. 다른 DB를 간접 변경하는 DUAL 작업은 순차 수행하라.
- 연결 View: create_view의 parent_page_id + data_source_id. database_id는 기존 DB에 View 탭을 추가할 때 사용하라.
- create_view 결과나 부모 fetch에서 연결 DB 블록 URL을 확보하라. saved view URL만 있으면 부모 본문에서 새 블록을 찾으라.
- 콘텐츠 편집: 최신 fetch의 정확한 old_str로 update_content를 호출하라. 현재 스키마에 따라 properties:{}와 content_updates를 함께 전달하라.

본문 첫 줄에 페이지 제목을 중복하지 마라. Date는 date:속성:start / end / is_datetime, Relation·Person은 배열을 사용하라. 표시명 ID / URL은 현재 SHOW 규약을 따르라. Created·Last Updated·Added Date·자동 번호·Formula·Rollup 값은 직접 쓰지 마라. Owner·Assignee는 확인된 사람만 넣으라.

## 관계와 진행률

Relation 에셋의 17개 선언 중 16개는 DUAL, Tasks.Parent Task만 단방향이다. Tasks.Project를 DUAL 'Tasks'로 선언하면 Projects.Tasks가 자동 생성된다. 역방향을 별도 ADD COLUMN으로 중복 생성하지 마라. 재실행 전 대상 data_source와 역속성을 확인하라.

Parent Task를 native sub-item이나 자동 Children 관계로 안내하지 마라. 사용자가 필요로 하면 현재 도구 지원을 확인하여 확장하라.

기본 Status는 선택값과 색상을 지정한 SELECT다. native STATUS를 만들었다고 주장하지 마라. 사용자가 native Status를 요구하면 옵션·그룹 지원을 확인한 뒤 수식·뷰와 함께 조정하라.

```
schema: "ID" UNIQUE_ID PREFIX 'TASK'
relation: ADD COLUMN "Project" RELATION('<새 Projects data_source UUID>', DUAL 'Tasks')
formula: ADD COLUMN "Completed" FORMULA('prop("Status") == "Done"')
rollup: ADD COLUMN "Progress" ROLLUP('Tasks', 'Completed', 'percent_checked')
count: ADD COLUMN "Task Count" ROLLUP('Tasks', 'Task', 'count')
```

count_all은 이 DDL에서 거부된 함수다. 집계는 count를 사용하라. Relation과 대상 속성이 존재한 뒤 Rollup을 만들라. Formula 속성 생성 성공과 실제 평가값 확인을 구분하라.

Progress 분모는 연결된 전체 Tasks다. Epic 제외·추정 가중치 기준은 요청받을 때만 변경하라. Tasks가 없을 때 빈 값 또는 0 표시는 실제 응답에 따라 설명하라.

Projects.Meeting Count는 Project에 연결된 회의록 복제 양식도 집계한다. 초기 집계 1을 실제 회의 1건으로 설명하지 마라. 실제 회의 수가 필요하면 Type!=Template 조건으로 확인하라.

## 연결 뷰

views.json의 29개 View는 모두 이번 Project로 필터한다. key로 연결 블록을 기록하라. SELECT 값이 유지되는 새 허브에는 configure를 그대로 치환해 사용하라.

| 화면 | 주요 조건 |
| --- | --- |
| 메인 Kanban | Project, Status 그룹, Due Date 오름차순 |
| My Tasks | Project, Assignee=me, Status!=Done |
| Sprint Tasks | Project, Sprint IS NOT EMPTY |
| Frontend / Backend | Project, Area |
| 회의 기록 / 양식 | Project, Type!=Template / Type=Template |
| AI 문서 | Project, Category in AI Prompt / AI Skill |
| 개발 문서 | Project, Architecture·Frontend·Backend·Database·API·QA·Version Control·Deployment·Infrastructure |
| QA·버전·배포 | Project, Category in QA / Version Control / Deployment |
| Figma Workspace | Project, Type=Figma, Role=Workspace |
| 바로가기 | Project, Role=Workspace |
| 개발 자료 | Project, Role in Reference/Learning, 개발 영역 |
| 경영 자료 | Project, Role in Reference/Learning, Area=Business |
| 학습 자료 | Project, Role=Learning, Status 그룹 |

Figma와 경영 자료의 Role 필터는 사용자와 합의한 자료 구분을 일관되게 적용한다. Sprint Tasks는 지정된 모든 Sprint의 업무다. Current Sprint라고 부르지 마라. 현재 스프린트 요청에는 실제 Active Sprint나 지원되는 동적 관계 필터를 확인하라.

Board에는 GROUP BY, Timeline에는 TIMELINE BY를 지정하라. Tasks.Start Date → Due Date, Sprints.Start → End를 사용하라. 빈 그룹·전체 너비처럼 도구에서 설정하지 못한 UI 옵션을 적용했다고 주장하지 마라.

FILTER의 Relation 값은 레코드 URL/UUID, Person 값은 me 또는 확인된 ID다. 사람·프로젝트 이름 문자열로 필터하지 마라. AND / OR 괄호를 유지하라.

## 페이지 편집과 재실행

쓰기 직전 fetch로 대상과 인접 구조를 확인하라. 요청한 부분만 최소 변경하고 구조 변경 후 다시 fetch하라.

- page 태그는 실제 자식이며 다른 페이지에 쓰면 이동할 수 있다. 계층을 유지할 위치에만 사용하라.
- mention-page는 이동 없는 링크다. Documents의 운영 가이드를 메뉴에서 참조할 때 사용하라.
- 메인 보드에는 연결 DB 블록 URL을 넣고 원본 Tasks 블록을 이동시키지 마라.
- 이미 create_view로 만든 블록은 url과 data-source-url을 보존하라. data-source-url만으로 중복 연결 블록을 추가하지 마라.
- DATABASE의 원본 child DB 태그를 보존하라.
- 새 페이지에 final_content를 적용할 수 있지만 기존 사용자 콘텐츠를 에셋 전체로 덮어쓰지 마라.
- 자식 삭제 경고에 자동으로 allow_deleting_content를 켜지 마라. 보존할 블록을 확인하여 안전한 수정으로 해결하라.
- 설명을 분리할 때는 새 문서의 내용 존재를 확인한 뒤 기존 설명을 제거하라.

부분 실패 시 생성된 항목을 지우고 재시작하지 마라. 마지막 성공 ID와 현재 상태를 비교하여 누락만 계속하라. 동일 이름이 여럿이면 부모·data_source·관계 대상으로 식별하고 모호한 대상만 확인하라.

## 검증과 중단 조건

실데이터 없는 상태에서는 스키마·필터·링크를 검증하라. 실업무처럼 보이는 시험 행을 만들지 마라. 검증용 계획은 실서버 쓰기를 수반하지 않게 하라.

isError·truncated·unknown_block_count·async_task를 확인하라. 비동기 작업은 성공 완료 후 종속 작업을 수행하라. Tool not found는 해당 기능을 현재 작업에서 재호출하지 마라. 권한 제한은 우회하지 말고 완료 범위와 막힌 동작을 설명하라.

오프라인 검증에서는 치환 완료, Relation 역속성, View가 쓰는 속성 존재, Project 필터, 원본 프로젝트 ID 미포함을 확인하라.
