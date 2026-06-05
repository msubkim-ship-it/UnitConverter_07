# 02 — UnitConverter_07 Spec 정합·RED 계획 세션 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_07 |
| 저장소 | https://github.com/msubkim-ship-it/UnitConverter_07 |
| 세션 일자 | 2026-06-05 |
| 브랜치 | `red` |
| 대응 Transcript | [Prompting/02-session-transcript.md](../Prompting/02-session-transcript.md) |
| 작성 | AI Agent 세션 산출물 정리 |

---

## 1. 세션 목적

01 세션에서 마련한 ECB·Dual-Track 설계를 **RED Phase 착수 전**에 정합한다.

- TC 묶음 갭(`D-LOC`, `U-IN`) PRD·reference formalize
- README·PRD·`.cursorrules`·`/review-ecb` SSOT 문구 통일
- `D-LOC-01`·`U-IN-01/02` **RED 계획표** 수립 (코드·테스트 본문 없음)
- spec 리뷰 반영 (`int[6]` 제거, `config/units.json` 샘플)

---

## 2. 수행 작업 요약

| # | 주제 | 산출·결과 |
|---|------|-----------|
| 1 | RED 계획 (entity) | `D-LOC-01` C2C·Track B·테스트 플랜 — `test_d_loc_01_blank_coords_row_major` |
| 2 | RED 계획 (boundary) | `U-IN-01`/`U-IN-02` Track A 표 — E003·E001 CLI 표면화 |
| 3 | README | TDD 6-커맨드 워크플로, TC 묶음, `config/` 반영 |
| 4 | PRD v0.2.0 | FR-LOC-01~03, FR-IN-01~02, D-LOC/U-IN, NFR-10~11 |
| 5 | reference.md | D-LOC-01~03, U-* TC ID SSOT 확장 |
| 6 | spec 리뷰 | `/review-ecb` 5항→4항, `ErrorCode` Enum 체크 |
| 7 | SSOT 통일 | `.cursorrules` — `constants.py` 단일 + JSON 로드용 |
| 8 | Harness | `config/units.json` 샘플 추가 |
| 9 | Hook | `session-init.sh` Enum·config·slash 커맨드 갱신 |
| 10 | Export | 본 보고서 + `02-session-transcript.md` |

---

## 3. 최종 산출물 목록

### 3.1 문서·설정

| 파일 | 역할 |
|------|------|
| `PRD.md` (v0.2.0) | FR-LOC/FR-IN, D-LOC/U-IN, §6.5 샘플 링크 |
| `README.md` | TDD 커맨드·TC 묶음·`config/units.json` |
| `.cursorrules` | MagicConstant SSOT 단일 문장 |
| `config/units.json` | boundary 로드용 샘플 |
| `reference.md` | D-LOC + U-* ID |

### 3.2 Cursor Agent

| 파일 | 역할 |
|------|------|
| `.cursor/commands/review-ecb.md` | `int[6]` 제거 → ErrorCode Enum 4항 체크 |
| `.cursor/commands/red-test-plan.md` | D-LOC·U-IN 묶음 참고 |
| `.cursor/hooks/session-init.sh` | SSOT·TDD 컨텍스트 갱신 |

### 3.3 기록

| 파일 | 역할 |
|------|------|
| `Report/02-session-report.md` | 본 보고서 |
| `Prompting/02-session-transcript.md` | 세션 대화 Export (34 turns) |

---

## 4. PRD·계약 정합 (핵심)

| 이슈 (01·transcript) | 조치 |
|---------------------|------|
| `D-LOC` / `FR-LOC` 미정의 | §3.5·§7.1·reference 추가 |
| `U-IN` / `FR-IN` 미정의 | §3.6·§7.2 추가 |
| `.cursorrules` 이중 SSOT | `constants.py` 단일 + JSON 로드용 |
| `/review-ecb` `int[6]` | **ErrorCode Enum (E001~E007)** 체크로 대체 |
| `config/units.json` 없음 | PRD §6.5 샘플 파일 생성 |

---

## 5. RED 계획 상태 (미구현)

| TC | 파일 (예정) | 다음 커맨드 |
|----|-------------|-------------|
| D-LOC-01 | `tests/entity/test_d_loc_01.py` | `/red-skeleton` |
| U-IN-01 | `tests/boundary/test_u_in.py` | `/red-skeleton` |
| U-IN-02 | 동일 | `/red-skeleton` |

> `src/`·`tests/` 본문은 본 세션에서 **미작성** (RED plan only).

---

## 6. 미완·다음 단계

| 우선순위 | 항목 |
|:--:|------|
| P0 | `/red-skeleton` — `D-LOC-01` 또는 `D-CONV-01` 실패 TC |
| P0 | `src/entity/constants.py`, `exceptions.py` GREEN 최소 구현 |
| P1 | `/red-skeleton` — `U-IN-01`/`U-IN-02` |
| P1 | Hook `afterFileEdit`(red→src 차단) |
| P2 | `git commit`·`staging` merge (사용자 요청 시) |

---

## 7. AI 활용 회고

| 도움이 된 점 | 한계 |
|-------------|------|
| PRD·README·rules·review-ecb 일괄 정합 | pytest RED FAIL 증거 없음 — Loop 미폐쇄 |
| LOC=SSOT 위치, IN=boundary 표면화 명확화 | `grid=None` 등 실습 루브릭 용어는 문서에 주석 필요 시 보강 |
| transcript Export 자동화 | jsonl 기준 34 turns; 이후 턴은 수동 append 가능 |

---

## 8. 관련 링크

- 이전 보고: [01-session-report.md](./01-session-report.md)
- Transcript: [../Prompting/02-session-transcript.md](../Prompting/02-session-transcript.md)
- Source: `agent-transcripts/30cd2237-92a4-48e6-9c30-5383e9420a45.jsonl`

---

작성자: 김명섭  
리뷰어: 김민주, 김소민, 김연우, 김정균, 김준호
