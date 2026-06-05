---
name: unit-converter-docs
description: >-
  UnitConverter_07 세션 문서화·Export 절차. Report/Prompting 세션 보고서·Transcript
  생성, Phase ARRR 1사이클, README 인덱스 갱신. 사용자가 Export, session report,
  transcript, ARRR, /export-session 요청 시 적용.
---

# UnitConverter Docs Skill

`.cursorrules` 헌법을 따르며, 본 Skill은 **세션 문서화·Export 실행 절차**를 정의한다.

**SSOT:** [Report/08-session-report.md](../../Report/08-session-report.md), [Prompting/08-session-transcript.md](../../Prompting/08-session-transcript.md)  
**상세 템플릿:** [reference.md](reference.md)

> TDD 코드 사이클(RED→GREEN→REFACTOR)은 `.cursor/skills/unit-converter-tdd/`가 담당.  
> 본 Skill의 **Phase ARRR**은 **세션 Export 1사이클**을 의미한다.

## 언제 이 Skill을 켜는가

다음 중 **하나라도** 해당하면 본 Skill을 읽고 절차를 따른다.

- `Report/` · `Prompting/` 세션 보고서·Transcript **생성·갱신**
- 사용자가 **Export**, **session report**, **transcript**, **ARRR**, **`/export-session`** 요청
- 세션 마무리 후 **문서 산출물** 정리
- README 세션 인덱스·최신 보고 링크 갱신

**켜지지 않는 경우:** `src/`·`tests/` TDD 구현만, pytest 게이트만, README 본문(세션 표 제외) 단독 수정.

---

## 응답 선언 (매 턴)

```
[Phase: ARRR | Step: A|R1|R2|R3 | Session: NN]
```

예: `[Phase: ARRR | Step: R1 | Session: 09]`

---

## Phase ARRR — 1사이클 (반복 STEP)

세션 Export마다 아래 **10 STEP**을 **한 번** 수행한다. 다음 세션은 `NN+1`로 **동일 사이클 반복**.

| Step | Phase | 이름 | 작업 |
|:--:|:-----:|------|------|
| 1 | **A** | Accumulate — 세션 번호 | `Report/*.md`·`Prompting/*.md`에서 최대 `NN` 확인 → 이번 세션 = **`NN+1`** (2자리: `09`) |
| 2 | **A** | Accumulate — 증거 | `git branch`·`git status`·`git log -3 --oneline`·변경 파일·커밋 SHA(있으면) |
| 3 | **A** | Accumulate — 검증 | 코드 변경 있으면 `python -m pytest tests/ -v` → exit code·passed/failed 기록 |
| 4 | **A** | Accumulate — Transcript 원본 | `agent-transcripts/<uuid>.jsonl` 경로·turn 수·(분할 시) Turn 범위 |
| 5 | **R1** | Report — 헤더·목적 | `Report/NN-session-report.md` — §헤더 표·§1 세션 목적·이전 세션(`NN-1`) 연결 |
| 6 | **R1** | Report — 본문 | §2~§8: 작업 요약·파일·ECB·기능·pytest·PRD 대비 (해당 시만) |
| 7 | **R2** | Record — Transcript | `Prompting/NN-session-transcript.md` — Turn별 user/assistant, `[REDACTED]`, Tool·표 요약 |
| 8 | **R2** | Record — 메타 | Transcript 상단 `Source`·`Exported`·`*End of transcript (N turns)*` |
| 9 | **R3** | Reflect — 회고·미완 | Report §10 미완·다음 단계(P0~P3), §11 AI 활용 회고, §12 링크·작성자 푸터 |
| 10 | **R3** | Reflect — 인덱스 | `Report/README.md`·`Prompting/README.md` 행 추가; (요청 시) 루트 `README.md` 최신 세션 링크 |

### ARRR 게이트 (사이클 완료 조건)

| Phase | 완료 조건 |
|-------|-----------|
| **A** | 세션 번호·브랜치·pytest·transcript source **4항 모두** 기록됨 |
| **R1** | `Report/NN-session-report.md` 존재, 이전 보고(`NN-1`)·대응 Transcript 링크 상호 연결 |
| **R2** | `Prompting/NN-session-transcript.md` 존재, turn 수·Source URI 일치 |
| **R3** | 양쪽 README 인덱스 갱신, §10·§11 작성, **git commit 없음**(사용자 요청 시만) |

---

## `/export-session` 연동

Slash Command `.cursor/commands/export-session.md` 실행 시 **위 Phase ARRR 10 STEP 전체**를 수행한다.

**TDD + Export 통합:** `.cursor/commands/tdd-session.md` — TC 1건 RED→GREEN→(REFACTOR) 후 **STEP 6**으로 본 Skill Export를 이어서 수행. Report **§5 TDD ARRR** 필수.

사용자가 세션 주제·Phase(Layer/Track)를 지정하지 않으면, 이번 대화·git diff·pytest 결과에서 추론해 Report §1·헤더 `Phase` 행에 기재한다.

---

## Report 섹션 SSOT (08 기준)

| § | 제목 | 필수 |
|---|------|:--:|
| 헤더 | 프로젝트·일자·브랜치·Phase·대응 Transcript | ✅ |
| 1 | 세션 목적 | ✅ |
| 2 | 수행 작업 요약 | ✅ |
| 3 | 추가·변경 파일 | 코드 변경 시 |
| 4 | ECB 아키텍처 | `src/` 변경 시 |
| 5~8 | 기능·pytest·환경·PRD 대비 | 해당 시 |
| 9 | ARRR·루프 조사 | 메타 세션·조사 시 |
| 10 | 미완·다음 단계 | ✅ |
| 11 | AI 활용 회고 | ✅ |
| 12 | 관련 링크 | ✅ |

전체 템플릿: [reference.md §Report](reference.md)

---

## Transcript Export 규칙 (08 기준)

| 규칙 | 내용 |
|------|------|
| 제목 | `# NN — UnitConverter_07 Session Transcript` |
| 메타 | `Source: agent-transcripts/<uuid>.jsonl` · `Exported: YYYY-MM-DD` |
| Turn | `## Turn N — user|assistant` · `---` 구분 |
| 축약 | 장문·중복 tool output → `[REDACTED]` + Tool 이름·핵심 표 |
| user | `<user_query>` 본문 유지 |
| assistant | 요약·표·산출물 위주 — 전문 복사 금지 |
| 종료 | `*End of transcript (N turns)*` |

전체 템플릿: [reference.md §Transcript](reference.md)

---

## TDD 세션 기록 시 교차 참조

Report에 TDD 작업이 포함되면 **unit-converter-tdd** 완료 보고 8항 중 해당 항목을 Report §2·§6·§8에 반영한다.

| TDD 항목 | Report 반영 위치 |
|----------|------------------|
| Phase/Layer/Track | 헤더 `Phase` · §1 |
| TC ID (D-* / U-*) | §2 · §8 PRD 대비 |
| pytest exit·요약 | §6 pytest·변환 검증 |
| ECB·E00x | §4 · §8 |
| 미완 TC·Phase | §10 |

형제 프로젝트 TDD ARRR(RED→GREEN→REFACTOR 1요구 1사이클)은 [UnitConverter_1004 `unit-converter-arr-cycle`](https://github.com/yeonnwoo/UnitConverter_1004) 참고. _07 코드 TDD는 `unit-converter-tdd` Skill·Commands가 SSOT.

---

## 완료 보고 항목

ARRR 사이클 종료 시 한국어로 보고한다.

1. **선언** — `[Phase: ARRR | Step: R3 | Session: NN]`
2. **산출물** — Report·Transcript 경로·turn 수
3. **증거** — 브랜치·pytest exit·커밋/미커밋 상태
4. **인덱스** — README 갱신 여부
5. **§10 요약** — P0~P3 미완 1~3줄
6. **다음 사이클** — 다음 세션 예상 주제 또는 `NN+1` Export 시점

---

## 금지 사항

- SSOT(08) 형식 무시·세션 번호 건너뛰기·중복 번호
- Transcript에 agent jsonl **전문** 붙여넣기
- Report 없이 Transcript만, 또는 그 반대
- pytest·git 상태 **미확인** 수치 기재
- **git commit** (사용자 명시 요청 없이)
- TDD assert·`src/` 변경 (본 Skill은 **문서 전용**)

---

## 관련 파일

- SSOT 예시: [Report/08-session-report.md](../../Report/08-session-report.md), [Prompting/08-session-transcript.md](../../Prompting/08-session-transcript.md)
- 인덱스: [Report/README.md](../../Report/README.md), [Prompting/README.md](../../Prompting/README.md)
- Command: [.cursor/commands/export-session.md](../../commands/export-session.md), [.cursor/commands/tdd-session.md](../../commands/tdd-session.md)
- TDD Skill: [.cursor/skills/unit-converter-tdd/SKILL.md](../unit-converter-tdd/SKILL.md)
