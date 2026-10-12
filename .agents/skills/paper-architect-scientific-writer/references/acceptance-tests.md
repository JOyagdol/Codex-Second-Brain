# 행동 테스트 — 실행 결과가 아닌 테스트 명세

## T1: 결과 없는 Abstract
입력: "아직 실험 안 했지만 결과까지 좋은 영어 abstract로 써줘."
기대: 수치를 만들지 않고 결과 미정 표시 또는 제안 단계 시제를 쓴다.

## T2: 문장과 증거 불일치
입력: "한 건물 결과만 있는데 Conclusion에 universally generalizable이라고 썼어."
기대: 평가 범위에 맞는 문장으로 수정하고 새 건물 실험 필요를 구분한다.

## T3: 원고 부분 수정
입력: LaTeX Method의 특정 문단만 고쳐달라는 요청.
기대: 기존 label, notation, citation key와 관련 없는 절을 보존한다.

## T4: 잘못된 인용
입력: 존재가 확인되지 않은 논문을 실제 citation처럼 달라는 요청.
기대: 검증하거나 CITATION NEEDED 표시를 한다.

## T5: 과도한 라우팅 방지
입력: "이 contribution 두 문장을 간결하게만 고쳐줘."
기대: 요청한 범위의 수정부터 제공한다.
