# TDD Session — TC 1건 RED→GREEN→(REFACTOR)→Export

UnitConverter_07 **TC당 1채팅** 통합 사이클. 대상 TC ID **1건**에 대해 TDD 전 Phase를 순서대로 수행한 뒤 **세션 Export**까지 마친다.

**선행 Skill:** `.cursor/skills/unit-converter-tdd/SKILL.md`  
**Export Skill:** `.cursor/skills/unit-converter-docs/SKILL.md` (마지막 Phase)

## 사용법

```
/tdd-session <TC-ID>
```

예:

```
/tdd-session D-LOC-02
/tdd-session D-CONV-01
/tdd-session U-IN-02
```

### 옵션 (프롬프트에 함께 적으면 적용)

| 옵션 | 효과 |
|------|------|
| `--no-refactor` | GREEN 후 REFACTOR·`/refactor-smell` 생략 |
| `--no-export` | TDD만 수행, `/export-session` 생략 |
| `--no-golden` | UI Track이어도 `/golden-master` 생략 |

옵션 없으면 **전체 사이클**(REFACTOR는 스멜 있을 때만, UI는 golden diff 제시).

## 필수 선언

**응답 첫 줄** (TC ID로 Layer·Track 확정 후):

```
Phase: tdd-session | TC: <TC-ID> | Layer: entity|control|boundary | Track: Logic|UI
```

Phase 전환 시마다 추가 선언:

```
Phase: red | Layer: … | Track: …
Phase: green | …
Phase: refactor | …   (해당 시)
Phase: ARRR | Step: A | Session: NN   (Export 시)
```

## TC ID 해석 (SSOT)

`.cursor/skills/unit-converter-tdd/reference.md` · [PRD.md](../../PRD.md) §7 기준.

| TC ID 패턴 | Layer | Track | 예상 테스트 파일 |
|------------|-------|-------|------------------|
| `D-LOC-*` | entity | Logic | `tests/entity/test_d_loc_XX.py` |
| `D-CONV-*` | control | Logic | `tests/control/test_d_conv_XX.py` |
| `D-ERR-*` | control | Logic | `tests/control/test_d_err_XX.py` |
| `D-REG-*` | control | Logic | `tests/control/test_d_reg_XX.py` |
| `U-*` | boundary | UI | `tests/boundary/test_u_*.py` |

**TC ID 미지정** 시 Report 최신 §10 P0 우선 — 현재 후보: **D-LOC-02** → D-LOC-03 → D-CONV-01.

### 선행 TC (게이트)

| TC ID | 선행 |
|-------|------|
| D-LOC-02 | D-LOC-01 ✅ |
| D-LOC-03 | D-LOC-02 |
| D-CONV-01~06 | D-LOC-03 권장 |
| D-ERR-01~06 | D-LOC-02 (ErrorCode SSOT) |
| U-IN-02 | D-LOC-02, D-ERR-01 |
| U-IN-01 | D-ERR-03 |
| U-CLI-01 | D-CONV-01~06, D-ERR-01~05 |

선행 미충족 시 **중단**하고 부족 TC ID를 보고한다.

---

## 통합 절차 (한 채팅 내 순차 실행)

각 Phase **게이트 통과 전** 다음 Phase로 넘어가지 않는다.

### STEP 1 — RED Plan (`/red-test-plan` 동등)

1. **브랜치** — `red` 확인. 아니면 전환 제안 후 중단.
2. **대상 TC** — 사용자 인자 또는 §10 P0 기본값 1건.
3. **계획표** — FR·Layer·Track·파일·함수명·Act·Assert 1줄 (코드·파일 생성 **금지**).
4. **보고** — 계획표 표 출력.

### STEP 2 — RED Skeleton (`/red-skeleton` 동등)

1. `tests/{layer}/` 에 **실패 assert**만 작성 (`src/` 수정 금지).
2. Logic: `ErrorCode.E00x` assert — 메시지 문자열 하드코딩 금지.
3. UI: stdin/stdout Mock 허용 — control·entity Mock **금지**.
4. **pytest FAIL**

```powershell
python -m pytest tests/{layer}/test_<target>.py -v
```

**RED 게이트:** exit ≠ 0. exit = 0이면 RED 미완 — assert 강화.

### STEP 3 — GREEN (`/green-minimal` 동등)

1. **브랜치** — `green` (전환 제안 후 진행).
2. `src/{layer}/` **최소 구현** — 대상 TC 통과에 필요한 코드만.
3. ECB·`constants`/`exceptions` SSOT·E00x raise 레이어 준수.
4. **pytest PASS**

```powershell
python -m pytest tests/{layer}/ -v
python -m pytest tests/ -v
```

**GREEN 게이트:** exit = 0.

### STEP 4 — REFACTOR (선택, `--no-refactor` 시 생략)

1. `/refactor-smell` 동등 — `src/` 스멜 표만 (수정 없음).
2. **P0/P1 스멜이 있을 때만** `/refactor-safe` — 브랜치 `refactoring`, `tests/` 동결.
3. 스멜 없으면 **「REFACTOR 생략」** 1줄 보고 후 STEP 5로.
4. **pytest PASS** 유지.

### STEP 5 — Golden (UI Track만, `--no-golden` 시 생략)

1. U-* GREEN 직후 `/golden-master` 동등.
2. golden 파일 **쓰기 금지** — diff만 제시, 사용자 승인 대기.
3. Logic Track(D-*)는 **Golden N/A** 1줄 기록.

### STEP 6 — Export (`/export-session` 동등, `--no-export` 시 생략)

`.cursor/commands/export-session.md` **Phase ARRR 10 STEP** 전체 수행.

**추가 필수:** Report **§5 TDD ARRR 1사이클** — 이번 `<TC-ID>` 기준:

| 소절 | 기록 |
|------|------|
| RED | Test ID·Layer/Track·pytest 명령·exit·FAIL 요약 |
| GREEN | PASS ID·변경 `src/`·exit |
| REFACTOR | 스멜·조치 또는 「생략」 |
| Golden | matched / diff / N/A |
| pytest | `python -m pytest tests/ -v` exit·passed 요약 |

Report §1·헤더 `Phase`에 `TDD Session — <TC-ID>` 기재.

---

## 최종 보고 (한국어)

| 항목 | 내용 |
|------|------|
| 선언 | `Phase: tdd-session \| TC: …` → 마지막 `Phase: ARRR \| Step: R3 \| Session: NN` |
| TC | 완료한 D-* / U-* |
| TDD | RED exit·GREEN exit·REFACTOR 여부·Golden 판정 |
| pytest | 최종 명령·exit code·passed/failed |
| 변경 파일 | `tests/` · `src/` · `Report/` · `Prompting/` |
| ECB·E00x | 위반 없음 / 해당 코드 |
| 산출물 | `Report/NN-session-report.md` · `Prompting/NN-session-transcript.md` |
| §10 | P0~P3 미완 1~3줄 |
| 다음 | 다음 `/tdd-session <TC-ID>` 제안 1건 |

---

## 금지

- assert 완화·삭제·`skip`·`xfail`·`NotImplementedError` stub으로 green
- RED에서 `src/` 수정
- Logic Track domain Mock
- MagicConstant 리터럴 산재 (`entity/constants.py` SSOT만)
- Golden Master **무단** 생성·갱신
- Export 시 Transcript jsonl **전문** 복사
- **git commit** (사용자 명시 요청 없이)
- Phase 게이트 미통과 시 다음 STEP 진행

---

## SSOT·참고

| 파일 | 역할 |
|------|------|
| `.cursor/skills/unit-converter-tdd/SKILL.md` | RED/GREEN/REFACTOR 절차 |
| `.cursor/skills/unit-converter-tdd/reference.md` | D-* / U-* ID |
| `.cursor/skills/unit-converter-docs/SKILL.md` | Export ARRR |
| `.cursor/commands/export-session.md` | STEP 6 상세 |
| `Report/09-session-report.md` §5·§7 | TDD 보고·Ask(RED) 후보 형식 |
