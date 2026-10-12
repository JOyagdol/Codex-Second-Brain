# 스킬 원본과 설치본 동기화

## 권한과 범위

현재 사용자 요청으로 승인된 스킬 유지·기록·저장 범위에서 실행합니다. 이 문서만으로 다른 저장소, 연구 코드, 공유 설정 또는 외부 연락 권한이 생기지 않습니다. 인증·호스트 정책·branch 보호를 우회하지 않습니다.

## 한 번의 업데이트 요청 처리

1. Git 원본의 최신 head와 변경할 설치 스킬을 읽습니다. 스킬 name을 기준으로 호스트 ID와 대응합니다. 한쪽의 변경을 다른 쪽에 무조건 덮어쓰지 않습니다.
2. 반복 사용할 규칙만 원본에 반영합니다. 연구 상태와 개인 링크는 Notion/개인 설정에 기록합니다. 공통 기억 문서는 7개 스킬에서 일치시킵니다.
3. validate, audit, 변경에 관련된 테스트를 실행합니다. diff와 공개 범위를 확인합니다.
4. 작업한 파일만 stage하고 commit/push합니다. 연결된 GitHub 도구로 tree/commit/ref를 갱신하는 방식도 가능합니다. 예상 head를 확인하고 원격이 바뀌면 다시 읽습니다.
5. ChatGPT Work에서는 원래 설치된 스킬의 ID/name을 유지하고 호스트 skill-creator 지침으로 저장합니다. 여러 스킬은 ID별로 하나씩 commit/push하여 순차 저장합니다. 한 번의 요청 안에서 처리할 수 있지만 설치 저장 push에 여러 스킬을 묶지 않습니다. 해당 호스트의 스킬 Git 저장 성공을 확인합니다. 사용자 GitHub push만으로 ChatGPT 설치가 끝난 것으로 표시하지 않습니다.
6. Codex PC에서는 clean checkout에서 `sync`를 실행하거나 pull 후 `install`합니다. 설치 파일이 개인적으로 수정되었으면 중단하고 병합합니다. 이미 열린 세션의 스킬 내용이 갱신되었는지는 별도로 확인하고 필요하면 새 세션을 엽니다.
7. Notion 세션에 원본 commit, 변경 이유, 적용된 환경, 미완료 환경을 남깁니다.

각 시스템 사이에 원자적 트랜잭션은 없습니다. 실패한 단계는 같은 commit에서 이어서 적용하고 성공한 저장을 거짓으로 되돌려 보고하지 않습니다.

## 안전한 Git push 도구

```bash
python3 scripts/second_brain.py publish --message "Update research workflow" --paths AGENTS.md docs/MEMORY_PROTOCOL.md
```

위 경로는 예시이며 실제 수정한 파일을 정확히 지정합니다. 이미 staged된 작업이 있거나 원격이 앞서 있으면 중단합니다. 이 도구는 기존 공개 파일의 명시적 변경을 처리합니다. 파일 삭제·이름 변경·보호 branch의 PR은 diff를 검토한 뒤 표준 Git/GitHub 절차로 수행합니다. push 재시도 시 원격 head를 먼저 확인합니다. `.gitignore`를 무시하는 강제 add를 사용하지 않습니다.

## Git 없이 ZIP만 사용하는 경우

`install`은 가능합니다. `sync`와 `publish`는 Git checkout이 필요합니다. clone한 폴더에 개인 설정만 복사한 뒤 다시 설치하면 같은 관리 사본으로 이어갑니다. 기존 파일의 내용이 같으면 중복 덮어쓰기 없이 채택합니다.

## 완료 상태

| 대상 | 완료 근거 |
| --- | --- |
| GitHub | 원격 branch가 반환한 commit을 가리킴 |
| ChatGPT | 설치 스킬 저장 성공 + 수정 내용 확인 |
| Notion | 저장된 page/row ID와 내용 확인 |
| Codex PC | 설치 스크립트 성공 + 스킬 로드 확인 |
| 맥락 연결 | 실제 Notion Research State fetch 성공 |

## 실패시 인계

Notion 불가 시 `private/pending/`에 세션 ID를 포함한 최소 기록을 남기고 공개 Git에 넣지 않습니다. 저장 응답이 불확실하면 같은 ID를 조회합니다. 두 AI가 현재 상태를 수정할 때는 기록 추가를 먼저 하고 State를 재조회합니다. 편집 시각이 달라졌으면 병합하며, 합의되지 않은 충돌은 Pending sync로 남깁니다.
