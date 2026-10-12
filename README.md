# Codex Second Brain

ChatGPT와 Codex에서 같은 연구 스킬과 Notion 기억을 사용하는 개인 연구 작업환경입니다.

- **Git**: 스킬·공통 운영 규칙·설치 도구의 원본.
- **Notion**: 프로젝트별 Research State, AI Sessions, Decisions, 기존 Literature.
- **실험 저장소**: 코드·config·run·원고의 실제 근거. 이 저장소는 실험 구현 저장소가 아닙니다.

## 빠른 시작

개인 전달 ZIP을 풀고 Codex에서 그 폴더를 연 다음 `START_HERE.md`를 읽고 설치해 달라고 요청하세요. ZIP에는 개인 연결 설정이 들어 있으므로 공개 업로드하지 않습니다. 저장소에서 직접 clone한 사본에는 개인 연결 설정이 없습니다.

Windows PowerShell (Python 3.10+):

```powershell
py -3 scripts/second_brain.py doctor
py -3 scripts/second_brain.py install --scope user
```

macOS/Linux:

```bash
python3 scripts/second_brain.py doctor
python3 scripts/second_brain.py install --scope user
```

사용자 설치는 `~/.agents/skills`에 7개 스킬을 복사하고, Codex home의 `AGENTS.md`에 연구 작업용 안내 블록을 추가합니다. 기존 내용은 보존합니다. 개인 Notion 연결 설정은 Codex home의 `second-brain/notion.json`에 복사합니다. `CODEX_HOME`이 있으면 그 경로를 사용하고, 없으면 `~/.codex`를 사용합니다. 설정 파일은 토큰을 포함하지 않습니다.

특정 프로젝트에만 설치하려면 `install --scope project --target <프로젝트_경로>`를 사용하세요. 사용자 설치와 프로젝트 설치를 동시에 하면 동일한 name의 스킬이 중복 표시될 수 있으므로 하나를 선택하세요. 이 저장소 안에서만 사용할 경우 이미 `.agents/skills`가 있어 복사 설치 없이 발견됩니다.

## Notion 연결 — 최초 1회

Codex에서 `codex mcp list`로 기존 연결을 확인합니다. Notion이 없다면 다음을 실행합니다.

```bash
codex mcp add notion --url https://mcp.notion.com/mcp
codex mcp login notion
```

OAuth 화면은 사용자가 완료해야 합니다. 기존 `notion` 서버가 다른 URL을 사용하면 임의로 덮어쓰지 말고 그 설정을 먼저 확인합니다. 이 저장소의 `.codex/config.toml`에도 같은 공개 MCP 주소가 들어 있습니다. 실제 인증·읽기·쓰기 가능 여부는 Notion 페이지 fetch로 확인합니다.

## 포함 스킬

| name | 역할 |
| --- | --- |
| world-graph-research-partner | 연구 맥락과 전문 검토 종합 |
| research-gap-positioning | 관련연구·연구 갭·novelty |
| experiment-designer-evaluator | 가설·baseline·ablation·평가 |
| paper-architect-scientific-writer | 논문 구조·문장·claim–evidence |
| top-tier-research-reviewer | 비판적 리뷰·rebuttal·제출 위험 |
| draft-invention-disclosure | 발명신고서와 기술 근거 |
| notion-project-template | 연구·프로젝트 허브 구성 지원 |

각 스킬은 자신의 전문 작업과 공통 기억 규칙을 함께 사용합니다. 개인 연구 사실은 공개 SKILL.md에 누적하지 않습니다.

## 계속 업데이트하기

지속 사용에는 Git clone을 권장합니다. ZIP에는 `.git` 이력이 없습니다.

```bash
git clone https://github.com/JOyagdol/Codex-Second-Brain.git
```

ZIP의 `config/notion.local.json`을 clone한 폴더의 같은 위치에 복사하고 그 폴더에서 다시 `install`하세요. 기존 설치와 동일한 파일은 그대로 유지합니다. Git 원본을 받아 설치 사본까지 갱신하려면:

```bash
python3 scripts/second_brain.py sync --scope user
```

`sync`는 원격에서 fast-forward로 받아 설치하는 명령입니다. Notion 기록은 연결된 AI가 공통 규칙에 따라 수행합니다. ChatGPT 설치본을 원격에서 자동 변경하는 API나 대화 밖 상시 실행 서비스는 이 저장소에 포함되지 않습니다.

## 작업 규칙과 문서

- [AGENTS.md](AGENTS.md): 저장소 작업 규칙
- [기억 운영](docs/MEMORY_PROTOCOL.md): 시작·체크포인트·인계·충돌 처리
- [배포와 동기화](docs/SYNC.md): Git, ChatGPT, Codex, Notion별 완료 조건
- [Notion 구성](docs/NOTION.md): 필드와 기록 템플릿
- `templates/`: 세션, 결정, 현재 상태 양식
- `config/notion.example.json`: 빈 연결 설정 예시

## 검증

```bash
python3 scripts/second_brain.py validate
python3 scripts/second_brain.py audit
python3 -m unittest discover -s tests -v
```

`audit`는 알려진 토큰과 개인 주소 패턴을 검사합니다. 공개해도 되는 내용인지에 대한 사람/에이전트의 검토를 대신하지 않습니다. 설치는 충돌을 먼저 검사하고 사용자 수정이 있으면 중단합니다. 이전 버전의 파일을 임의 삭제하지 않으며, 삭제·이름 변경이 필요한 업데이트는 별도로 검토합니다.

## 확인한 공식 문서

확인일: 2026-10-12. 호스트 버전에 따라 달라질 수 있습니다.

- [Codex Skills](https://learn.chatgpt.com/docs/build-skills)
- [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [Notion MCP 연결](https://developers.notion.com/guides/mcp/get-started-with-mcp)
