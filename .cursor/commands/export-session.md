# Export Session — Report·Transcript 세션 Export

UnitConverter_07 **세션 문서 Export**만 수행한다. `.cursor/skills/unit-converter-docs/SKILL.md`의 **Phase ARRR 1사이클(10 STEP)** 을 따른다. **코드·테스트 수정 금지.**

## 필수 선언

**응답 첫 줄:**

```
Phase: ARRR | Step: A | Session: NN
```

세션 번호 `NN`은 STEP 1에서 확정 후 선언에 반영한다.

## Phase ARRR — 10 STEP (1사이클)

### A — Accumulate (STEP 1~4)

1. **세션 번호** — `Report/`·`Prompting/` 최대 번호 + 1 → `NN` (예: `09`)
2. **git 증거** — `git branch` · `git status` · `git log -3 --oneline`
3. **pytest** — 이번 세션에 `src/`·`tests/` 변경이 있으면:

```powershell
python -m pytest tests/ -v
```

exit code·passed/failed를 Report §6에 기록.

4. **Transcript 원본** — 현재 세션 `agent-transcripts/<uuid>.jsonl` 경로·turn 수 확인

### R1 — Report (STEP 5~6)

5. **헤더·§1** — [Report/08-session-report.md](../../Report/08-session-report.md) 형식
6. **§2~§8** — 작업 요약·파일·ECB·pytest·PRD 대비 ([reference.md](../../skills/unit-converter-docs/reference.md))

산출: `Report/NN-session-report.md`

### R2 — Record (STEP 7~8)

7. **Turn Export** — [Prompting/08-session-transcript.md](../../Prompting/08-session-transcript.md) 형식  
   - `[REDACTED]` + Tool·표 요약  
   - jsonl 전문 붙여넣기 **금지**
8. **메타** — Source · Exported 날짜 · `*End of transcript (N turns)*`

산출: `Prompting/NN-session-transcript.md`

### R3 — Reflect (STEP 9~10)

9. **회고** — Report §10 미완(P0~P3) · §11 AI 활용 회고 · §12 링크·푸터
10. **인덱스** — `Report/README.md` · `Prompting/README.md` 행 추가  
    (사용자 요청 시) 루트 `README.md` 최신 세션 링크 갱신

## ARRR 게이트

| Phase | 통과 조건 |
|-------|-----------|
| A | 번호·git·pytest·source 4항 기록 |
| R1 | Report 파일·상호 링크 |
| R2 | Transcript 파일·turn 수 일치 |
| R3 | README 인덱스·§10·§11 완료 |

## 보고

작업 종료 시 한국어로 보고한다:

| 항목 | 내용 |
|------|------|
| 선언 | `Phase: ARRR \| Step: R3 \| Session: NN` |
| 산출물 | Report·Transcript 경로 |
| turn 수 | Transcript N turns |
| pytest | 명령·exit code (해당 시) |
| git | 브랜치·커밋/미커밋 |
| §10 | P0~P3 요약 1~3줄 |
| 다음 | `NN+1` Export 시점 또는 후속 작업 |

## 금지

- `src/` · `tests/` · `pyproject.toml` **수정** (문서·README 인덱스만)
- 세션 번호 건너뛰기·SSOT(08) 형식 무시
- pytest·git **미확인** 수치
- Transcript jsonl **전문** 복사
- **git commit** (사용자 명시 요청 없이)

## SSOT·참고

- Skill: `.cursor/skills/unit-converter-docs/SKILL.md`
- 템플릿: `.cursor/skills/unit-converter-docs/reference.md`
- 예시: `Report/08-session-report.md`, `Prompting/08-session-transcript.md`
