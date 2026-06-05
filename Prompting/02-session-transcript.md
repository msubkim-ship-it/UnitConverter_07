# 02 — UnitConverter_07 Session Transcript
> Source: agent-transcripts/30cd2237-92a4-48e6-9c30-5383e9420a45.jsonl
> Exported: 2026-06-05

---

## Turn 1 — user

<cursor_commands>

--- Cursor Command: red-test-plan ---
# RED Test Plan — TC 계획만 (코드·테스트 본문 없음)

UnitConverter_07 **RED 선행 단계**: 이번 사이클에 작성할 TC **계획표**만 만든다.  
`.cursorrules`, [PRD.md](../../PRD.md), `.cursor/skills/unit-converter-tdd/reference.md` 기준.

**다음 커맨드:** `/red-skeleton`

## 필수 선언

```
Phase: red-plan | Layer: entity|control|boundary | Track: Logic|UI
```

## 절차

1. **브랜치** — `red` 브랜치 확인. 아니면 전환 제안 후 중단.
2. **범위 확인** — 사용자 지정 TC ID가 없으면 **M1 P0 우선**: `D-CONV-01` → `D-ERR-03` 순 제안.
3. **PRD·reference 대조** — 각 TC에 FR-ID·Layer·Track·예상 실패 원인 1줄 매핑.
4. **파일 계획** — `tests/{layer}/test_d_*.py` 또는 `test_u_*.py` 경로·함수명만 설계.
5. **계획표 출력** — 하단 표 형식으로만 보고 (**파일 생성·수정 금지**).

## TC 계획표 (출력 형식)

| TC ID | FR | Layer | Track | 파일 | 테스트 함수 | Act 대상 (미구현 API) | Assert (실패 조건) | 우선순위 |
|-------|-----|-------|-------|------|-------------|----------------------|-------------------|----------|
| D-CONV-01 | FR-05 | entity | Logic | `tests/entity/test_d_conversion.py` | `test_d_conv_01_meter_to_feet` | `ConversionService.convert` | 결과 ≈ 8.2021… | P0 |

### Logic Track (D-*) 참고

| 묶음 | ID |
|------|-----|
| 변환 | D-CONV-01 ~ 06 |
| 등록 | D-REG-01 ~ 02 |
| 에러 | D-ERR-01 ~ 06 |

### UI Track (U-*) 참고 — [PRD §7.2](../../PRD.md)

`U-CLI-01`, `U-FMT-01/02`, `U-CFG-01`, `U-REG-01`

## 보고

| 항목 | 내용 |
|------|------|
| 선언 | `Phase: red-plan \| …` |
| 이번 사이클 TC | ID 목록 |
| 미착수 TC | reference·PRD 대비 남은 ID |
| 다음 | `/red-skeleton` 대상 파일·함수 |

## 금지

- `tests/`, `src/` **파일 생성·수정**
- 구현·assert 코드 작성
- pytest 실행 ( skeleton 이후 )
- **git commit** (사용자 요청 없이)

--- End Command ---

--- Cursor Command: red-skeleton ---
# RED Skeleton — 실패 테스트 골격 작성

`/red-test-plan` 계획을 바탕으로 **실패하는 테스트 골격**을 `tests/`에만 작성한다.  
`.cursorrules`, `.cursor/skills/unit-converter-tdd/` 기준. **다음:** `pytest FAIL` 확인 후 `/green-minimal`.

## 필수 선언

```
Phase: red | Layer: entity|control|boundary | Track: Logic|UI
```

## 절차

1. **계획 확인** — 직전 `/red-test-plan` 표 또는 사용자 지정 TC ID.
2. **브랜치** — `red` 브랜치 필수.
3. **파일·함수 생성** — `tests/{layer}/test_d_*.py` (Logic) 또는 `test_u_*.py` (UI).
4. **AAA 골격**
   - **Arrange**: 입력값·픽스처. MagicConstant는 `entity.constants` import 예정(아직 없으면 import로 ERROR 유도).
   - **Act**: `src.{layer}.*` API 호출 (미구현 → FAIL/ERROR).
   - **Assert**: FR·E00x 기준 **강한 assert** (Logic은 `ErrorCode.E00x`, 변환은 `pytest.approx`).
5. **TC 메타** — docstring 또는 `@pytest.mark`에 `D-CONV-01` 등 ID.
6. **pytest FAIL** — 대상 파일 실행, **exit ≠ 0** 확인.
7. **보고** — FAIL 요약·변경 `tests/` 경로만.

## pytest

```bash
pytest tests/entity/test_d_conversion.py -v
pytest tests/entity/ --collect-only -q
```

**RED 게이트:** FAILED 또는 ERROR ≥ 1, exit ≠ 0.

## 보고

| 항목 | 내용 |
|------|------|
| TC ID | 작성한 D-* / U-* |
| FAIL 요약 | TC명·ImportError/AssertionError 등 |
| 변경 파일 | `tests/`만 |
| pytest | 명령·exit code |
| 다음 | `/green-minimal` — 통과 대상 TC·Layer |

## 금지

- `src/` 수정·생성
- Logic Track **Domain Mock** (`MagicMock`, `patch` on Registry/Service)
- `skip`, `xfail`, `NotImplementedError` stub, assert 완화
- `tests/**/golden/**` 생성 (→ `/golden-master`)
- **git commit** (사용자 요청 없이)

으로 넘길 준비됐다고 한 줄로 알려줘.
--- End Command ---
</cursor_commands>
<user_query>

/red-test-plan
Phase: red | Layer: entity | Track: Logic
이번 RED 묶음: D-LOC-01 (FR-LOC-01)
다음을 표로 작성해줘. tests/·src/ 파일은 만들지 마.
1. C2C 추적 (Rule 1~3 적용)
   - PRD FR-LOC-01 인용 (docs/PRD.md)
   - To-Do 1개 (판단 포함 항목만)
   - Test ID → Given / When / Then
2. Track B (D-*) RED 설계표
   | Test ID | 대상 함수 | Given→Then | Invariant | Expected RED Failure |
3. 테스트 플랜
   - 파일: tests/entity/test_d_loc_01.py
   - test 함수명 후보
   - conftest 픽스처 (G1 격자 등, 로직 없음)
   - pytest 명령:
     python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
   - RED 묶음 범위 (이번 1~3 ID)
4. ECB·Mock 점검
   - Logic Track → Domain Mock 금지
   - entity E001~E005 emit 금지
금지: src/ 수정, GREEN/REFACTOR, skip/xfail
완료 후: /red-skeleton 으로 넘길 준비됐다고 한 줄로 알려줘.

</user_query>

---

## Turn 2 — assistant

RED 테스트 계획을 위해 PRD·reference·브랜치 상태를 확인합니다.

[REDACTED]

[Tool: Read, Glob, Grep, Shell]

---

## Turn 3 — assistant

[REDACTED]

[Tool: Read, Read, Grep, Glob]

---

## Turn 4 — assistant

[REDACTED]

[Tool: Glob, Grep, Read, Read]

---

## Turn 5 — assistant

[REDACTED]

[Tool: Grep, Grep, Glob]

---

## Turn 6 — assistant

[REDACTED]

[Tool: Read, Grep, Read]

---

## Turn 7 — assistant

[REDACTED]

[Tool: Grep, Glob, Glob]

---

## Turn 8 — assistant

[REDACTED]

[Tool: Read, Grep]

---

## Turn 9 — assistant

[REDACTED]

[Tool: Read, Grep]

---

## Turn 10 — assistant

[REDACTED]

[Tool: Shell, Grep]

---

## Turn 11 — assistant

**Phase: red-plan | Layer: entity | Track: Logic**

브랜치: `red` ✅  
파일 생성·수정: 없음

> **갭 알림:** `docs/PRD.md`는 워크트리에 없습니다. `FR-LOC-01` / `D-LOC-*`도 `PRD.md`·`reference.md`에 미등록입니다. 아래 C2C는 **PRD §2.3·§2.1(암묵 SSOT)** + 이전 세션에서 합의된 LOC=**Location/SSOT** 의미를 기준으로 작성했습니다.

---

## 1. C2C 추적 (Rule 1~3)

### Rule 1 — PRD FR-LOC-01 인용

| 항목 | 내용 |
|------|------|
| 경로 | `docs/PRD.md` ❌ → **`PRD.md`** §2.3·§2.1 인용 |
| FR-LOC-01 (정식 ID 없음 — 추적용 정규화) | 변환 비율·기준 단위 상수는 `src/entity/constants.py`에 **단일 정의(SSOT)** 하며, `config/units.json`은 boundary가 로드·주입하고, 수치를 코드·테스트에 **리터럴 복사 금지** |

**PRD 원문 (§2.3):**

> 변환 비율·기준 단위 상수는 `src/entity/constants.py`에 **단일 정의**한다.  
> `config/units.json`(또는 YAML)은 boundary가 로드하여 control에 주입하며, 수치를 코드·테스트에 **리터럴 복사 금지**.

**PRD 원문 (§2.1 — 검증 대상 수치):**

| 단위 | 비율 |
|------|------|
| meter | 1 (기준) |
| feet | 1 meter = **3.28084** feet |
| yard | 1 meter = **1.09361** yard |

### Rule 2 — To-Do 1개 (판단 포함)

| To-Do | 판단 |
|-------|------|
| **D-LOC-01 RED 골격에서 ratio SSOT를 `entity.constants` import로만 검증할지, row-major 격자 튜플(`G1`) fixture로 순서·값을 함께 assert할지 확정** | ✅ **격자 fixture + import 병행** — 테스트 본문에 `3.28084`/`1.09361` 리터럴 금지(LOC 불변식); `G1` fixture는 `constants` import 실패 시 ERROR, GREEN 후 `(1.0, FEET_PER_METER, YARD_PER_METER)` row-major 순서 assert |

### Rule 3 — Test ID → Given / When / Then

| Test ID | Given | When | Then |
|---------|-------|------|------|
| **D-LOC-01** | `tests/entity/conftest.py`의 **`g1_ratio_grid_row_major`** fixture 준비 (로직 없음, `entity.constants` import만 시도) | `test_d_loc_01_blank_coords_row_major`가 fixture·Act API 호출 | row-major 3-tuple `(meter_ratio, feet_ratio, yard_ratio) == (1.0, FEET_PER_METER, YARD_PER_METER)` — **리터럴 없이 constants 참조만** |
| D-LOC-02 *(묶음 2, 이번 skeleton 제외)* | `entity.exceptions.ErrorCode` SSOT 존재 | import `ErrorCode.E001`~`E007` | enum 멤버 7종 존재·코드 문자열 불변 |
| D-LOC-03 *(묶음 3, 이번 skeleton 제외)* | `entity.constants.BASE_UNIT` SSOT | import `BASE_UNIT` | 값 == `"meter"` (문자열 SSOT) |

---

## 2. Track B (D-*) RED 설계표

| Test ID | 대상 함수 | Given→Then | Invariant | Expected RED Failure |
|---------|-----------|------------|-----------|---------------------|
| **D-LOC-01** | `entity.constants` — `FEET_PER_METER`, `YARD_PER_METER`, `METER_RATIO`(또는 `RATIOS_ROW_MAJOR`) | Given: G1 row-major �격자 fixture · When: constants import + tuple 반환 Act · Then: `(1.0, FEET_PER_METER, YARD_PER_METER)` | 테스트·Act 본문 **MagicConstant 리터럴 0건**; entity는 stdlib만 import | `ModuleNotFoundError: entity.constants` 또는 `ImportError` ( `src/entity/constants.py` 미구현) |
| D-LOC-02 | `entity.exceptions.ErrorCode` | Given: — · When: `ErrorCode` import · Then: E001~E007 멤버 존재 | Logic Track **Domain Mock 금지**; E001~E005 **emit/assert 금지**(정의만) | `ModuleNotFoundError: entity.exceptions` |
| D-LOC-03 | `entity.constants.BASE_UNIT` | Given: — · When: `BASE_UNIT` import · Then: `"meter"` | BASE_UNIT 단일 SSOT | `ImportError` / `AttributeError: BASE_UNIT` |

---

## 3. 테스트 플랜

| 항목 | 내용 |
|------|------|
| **파일** | `tests/entity/test_d_loc_01.py` |
| **test 함수명 (후보)** | `test_d_loc_01_blank_coords_row_major` *(이번 skeleton)* · `test_d_loc_02_error_code_enum_ssot` · `test_d_loc_03_base_unit_ssot` |
| **conftest 픽스처** | `tests/entity/conftest.py`: **`g1_ratio_grid_row_major`** — `from entity.constants import FEET_PER_METER, YARD_PER_METER` 후 `(1.0, FEET_PER_METER, YARD_PER_METER)` 반환 (계산·변환 로직 없음). *(D-LOC-02/03용 `g2_error_code_ssot`, `g3_base_unit`은 후속 skeleton)* |
| **Act 대상 (미구현 API)** | `entity.constants.FEET_PER_METER`, `YARD_PER_METER`, (선택) `RATIOS_ROW_MAJOR` |
| **Assert (실패 조건)** | fixture tuple 길이 3, `g1[0]==1.0`, `g1[1]==FEET_PER_METER`, `g1[2]==YARD_PER_METER` — **pytest.approx 불필요**(동일 SSOT 참조) |
| **pytest 명령** | `python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v` |
| **RED 묶음 범위** | **D-LOC-01 ~ D-LOC-03** (이번 skeleton: **D-LOC-01만**) |

### TC 계획표 (표준)

| TC ID | FR | Layer | Track | 파일 | 테스트 함수 | Act 대상 (미구현 API) | Assert (실패 조건) | 우선순위 |
|-------|-----|-------|-------|------|-------------|----------------------|-------------------|----------|
| D-LOC-01 | FR-LOC-01 (§2.3) | entity | Logic | `tests/entity/test_d_loc_01.py` | `test_d_loc_01_blank_coords_row_major` | `entity.constants.*` | G1 row-major SSOT tuple | P0 |
| D-LOC-02 | FR-LOC-01 (§3.4) | entity | Logic | `tests/entity/test_d_loc_01.py` | `test_d_loc_02_error_code_enum_ssot` | `entity.exceptions.ErrorCode` | E001~E007 정의 | P0 |
| D-LOC-03 | FR-LOC-01 (§2.1) | entity | Logic | `tests/entity/test_d_loc_01.py` | `test_d_loc_03_base_unit_ssot` | `entity.constants.BASE_UNIT` | `"meter"` | P0 |

---

## 4. ECB·Mock 점검

| 점검 | 결과 |
|------|------|
| Logic Track → **Domain Mock 금지** | ✅ `MagicMock`/`patch` on Registry·Service **사용 안 함** — 실제 `entity.constants` import |
| entity import 방향 | ✅ stdlib + `entity.*` only; control/boundary import **금지** |
| entity **E001~E005 emit 금지** | ✅ D-LOC-01은 상수 SSOT만; 예외 raise·코드 assert **없음** (D-LOC-02는 enum **정의** import만) |
| MagicConstant 리터럴 | ✅ 테스트 본문 `3.28084`/`1.09361` **금지** — constants SSOT 경유 |
| skip/xfail/stub | ✅ **금지** |

---

## 보고

| 항목 | 내용 |
|------|------|
| 선언 | `Phase: red-plan \| Layer: entity \| Track: Logic` |
| 브랜치 | `red` |
| 이번 사이클 TC | **D-LOC-01** |
| RED 묶음 (1~3) | D-LOC-01, D-LOC-02, D-LOC-03 |
| 미착수 TC | D-CONV-01~06, D-REG-01~02, D-ERR-01~06, U-* 전부 · **D-LOC-02/03** (다음 skeleton) |
| PRD 갭 | `FR-LOC-01`/`D-LOC-*` formalize 필요 (`PRD.md` §7.1, `reference.md`) |
| 다음 `/red-skeleton` | `tests/entity/conftest.py` (`g1_ratio_grid_row_major`), `tests/entity/test_d_loc_01.py` (`test_d_loc_01_blank_coords_row_major`) |

---

**/red-skeleton**으로 넘길 준비됐습니다.

[REDACTED]

---

## Turn 12 — user

<cursor_commands>

--- Cursor Command: red-test-plan ---
# RED Test Plan — TC 계획만 (코드·테스트 본문 없음)

UnitConverter_07 **RED 선행 단계**: 이번 사이클에 작성할 TC **계획표**만 만든다.  
`.cursorrules`, [PRD.md](../../PRD.md), `.cursor/skills/unit-converter-tdd/reference.md` 기준.

**다음 커맨드:** `/red-skeleton`

## 필수 선언

```
Phase: red-plan | Layer: entity|control|boundary | Track: Logic|UI
```

## 절차

1. **브랜치** — `red` 브랜치 확인. 아니면 전환 제안 후 중단.
2. **범위 확인** — 사용자 지정 TC ID가 없으면 **M1 P0 우선**: `D-CONV-01` → `D-ERR-03` 순 제안.
3. **PRD·reference 대조** — 각 TC에 FR-ID·Layer·Track·예상 실패 원인 1줄 매핑.
4. **파일 계획** — `tests/{layer}/test_d_*.py` 또는 `test_u_*.py` 경로·함수명만 설계.
5. **계획표 출력** — 하단 표 형식으로만 보고 (**파일 생성·수정 금지**).

## TC 계획표 (출력 형식)

| TC ID | FR | Layer | Track | 파일 | 테스트 함수 | Act 대상 (미구현 API) | Assert (실패 조건) | 우선순위 |
|-------|-----|-------|-------|------|-------------|----------------------|-------------------|----------|
| D-CONV-01 | FR-05 | entity | Logic | `tests/entity/test_d_conversion.py` | `test_d_conv_01_meter_to_feet` | `ConversionService.convert` | 결과 ≈ 8.2021… | P0 |

### Logic Track (D-*) 참고

| 묶음 | ID |
|------|-----|
| 변환 | D-CONV-01 ~ 06 |
| 등록 | D-REG-01 ~ 02 |
| 에러 | D-ERR-01 ~ 06 |

### UI Track (U-*) 참고 — [PRD §7.2](../../PRD.md)

`U-CLI-01`, `U-FMT-01/02`, `U-CFG-01`, `U-REG-01`

## 보고

| 항목 | 내용 |
|------|------|
| 선언 | `Phase: red-plan \| …` |
| 이번 사이클 TC | ID 목록 |
| 미착수 TC | reference·PRD 대비 남은 ID |
| 다음 | `/red-skeleton` 대상 파일·함수 |

## 금지

- `tests/`, `src/` **파일 생성·수정**
- 구현·assert 코드 작성
- pytest 실행 ( skeleton 이후 )
- **git commit** (사용자 요청 없이)

--- End Command ---
</cursor_commands>
<user_query>
/red-test-plan
Phase: red | Layer: boundary | Track: UI
이번 RED 묶음: U-IN-01, U-IN-02
Track A 표: | Test ID | Given | Then | Expected RED Failure |
(U-IN-01 grid=None → E003, ModuleNotFoundError 등)
</user_query>

---

## Turn 13 — assistant

U-IN UI Track RED 계획을 위해 PRD·reference·기존 테스트 구조를 확인합니다.

[REDACTED]

[Tool: Grep, Grep, Shell, Glob]

---

## Turn 14 — assistant

[REDACTED]

[Tool: Grep, Read, Read]

---

## Turn 15 — assistant

[REDACTED]

[Tool: Glob, Read, Grep]

---

## Turn 16 — assistant

**Phase: red-plan | Layer: boundary | Track: UI**

브랜치: `red` ✅ · `tests/`·`src/` 미생성(계획만)

> **갭:** `U-IN-01`/`U-IN-02`는 `PRD.md` §7.2·`reference.md`에 없습니다. **IN = boundary 입력·에러 표면화** 묶음으로, Logic 대응 `D-ERR-03`/`D-ERR-01`·FR-10/FR-11과 쌍을 이룹니다. `grid=None`은 커스텀 Registry/설정 격자 미주입(기본 3단위) 시나리오로 해석했습니다.

---

## Track A — Given / Then / Expected RED Failure

| Test ID | Given | Then | Expected RED Failure |
|---------|-------|------|----------------------|
| **U-IN-01** | stdin(또는 `capsys`) 한 줄: `meter:-2.5` · Act: `boundary` 진입점 `run(input_line=…, grid=None)` (기본 Registry) | exit ≠ 0 · stdout/stderr에 **E003**에 대응하는 사용자 메시지 1줄 (메시지 SSOT: boundary mapper; 코드 문자열 `E003` 포함 또는 golden 대비 패턴) | `ModuleNotFoundError` / `ImportError` (`boundary.cli`, `CliApp`, `ErrorPresenter` 등 미구현) · 또는 `AssertionError`(메시지·exit code 미충족) |
| **U-IN-02** | stdin 한 줄: `meter2.5` (`:` 없음, `grid=None`) | exit ≠ 0 · **E001** 사용자 메시지 1줄 | 동일 — `ImportError` on boundary 모듈 · 또는 `AssertionError` |

---

## TC 계획표 (표준)

| TC ID | FR | Layer | Track | 파일 | 테스트 함수 | Act 대상 (미구현 API) | Assert (실패 조건) | 우선순위 |
|-------|-----|-------|-------|------|-------------|----------------------|-------------------|----------|
| U-IN-01 | FR-10 | boundary | UI | `tests/boundary/test_u_in.py` | `test_u_in_01_negative_input_e003` | `CliApp.run(..., grid=None)` 또는 `run_cli(line, grid=None)` | exit ≠ 0 + E003 메시지 | P0 |
| U-IN-02 | FR-11 | boundary | UI | `tests/boundary/test_u_in.py` | `test_u_in_02_missing_colon_e001` | 동일 진입점 | exit ≠ 0 + E001 메시지 | P0 |

---

## PRD·reference 대조

| TC ID | FR | 검증 항목 | Logic 쌍 | 예상 RED 원인 1줄 |
|-------|-----|-----------|----------|------------------|
| U-IN-01 | FR-10 | 음수 `meter:-2.5` 거부·표면화 | D-ERR-03 (control/entity E003) | `src/boundary/` 없음 → import FAIL |
| U-IN-02 | FR-11 | `:` 없는 형식 거부 | D-ERR-01 | boundary `InputParser`/`CliApp` 미구현 |

**PRD 인용 (§3.3·§3.4):**

- FR-10: 음수 입력 거부 → **E003**
- FR-11: 잘못된 형식 거부 (`:` 없음, 빈 입력, 숫자 아님) → **E001 / E002**
- boundary: 에러 **코드 → 사용자 메시지** 변환·출력만 담당

---

## 파일·픽스처·pytest (skeleton 대상)

| 항목 | 계획 |
|------|------|
| 파일 | `tests/boundary/test_u_in.py` |
| conftest | `tests/boundary/conftest.py` — `u_in_01_stdin`( `meter:-2.5` ), `u_in_02_stdin`( `meter2.5` ); **`grid=None` kwarg 고정** (로직 없음) |
| Mock | **stdin `monkeypatch` / `capsys`만 허용** · control·entity `MagicMock`/`patch` **금지** |
| pytest (skeleton 후) | `python -m pytest tests/boundary/test_u_in.py::test_u_in_01_negative_input_e003 -v` |
| | `python -m pytest tests/boundary/test_u_in.py::test_u_in_02_missing_colon_e001 -v` |

---

## ECB·Mock 점검

| 점검 | 결과 |
|------|------|
| UI Track I/O Mock | ✅ stdin/stdout·`capsys` 허용 |
| Domain Mock 금지 | ✅ `ConversionService`/`UnitRegistry` patch 금지 — 실제 boundary→control 경로(구현 후) |
| boundary import | ✅ control, entity만 (역방향 없음) |
| Logic vs UI 분리 | ✅ E003 raise는 control/entity; U-*는 **메시지·exit** assert |
| golden | ❌ 이번 묶음 제외 (`/golden-master` 후속) |

---

## 보고

| 항목 | 내용 |
|------|------|
| 선언 | `Phase: red-plan \| Layer: boundary \| Track: UI` |
| 브랜치 | `red` |
| 이번 RED 묶음 | **U-IN-01**, **U-IN-02** |
| 미착수 TC | PRD §7.2: U-CLI-01, U-FMT-01/02, U-CFG-01, U-REG-01 · Logic D-* 전부 · **U-IN-03+** (E002/E004 등 확장 시) |
| PRD 갭 | §7.2에 `U-IN-01`/`U-IN-02`·`FR-IN-*` formalize 권장 |
| 다음 `/red-skeleton` | `tests/boundary/conftest.py`, `tests/boundary/test_u_in.py` — 위 2 함수 |

**/red-skeleton**으로 넘길 준비됐습니다.

[REDACTED]

---

## Turn 17 — user

<user_query>
README.md 파일 업데이트해줘.
</user_query>

---

## Turn 18 — assistant

README와 프로젝트 현황을 확인한 뒤 README를 갱신합니다.

[REDACTED]

[Tool: Read, Glob, Glob, Glob]

---

## Turn 19 — assistant

[REDACTED]

[Tool: Glob, Read]

---

## Turn 20 — assistant

README에 TDD 워크플로·TC 묶음·프로젝트 구조를 반영해 갱신합니다.

[REDACTED]

[Tool: Write]

---

## Turn 21 — assistant

`README.md`를 현재 프로젝트 상태에 맞게 갱신했습니다.

### 주요 변경
- **구조** — `Report/`, `Prompting/`, `.cursor/commands/` 8개 반영, Harness(`red` 브랜치·`src/`/`tests/` 진행 중) 안내
- **TDD 워크플로** — `/red-test-plan` → … → `/refactor-safe` 순서와 각 커맨드 역할 표
- **TC ID** — PRD 공식(`D-CONV`/`D-ERR`/`U-CLI` 등) + 진행 중 묶음(`D-LOC`, `U-IN`) 구분
- **입력 검증 예시** — `meter:-2.5`(E003), `meter2.5`(E001) 표 추가
- **문서 링크** — `Report/01-session-report.md`, Skill·reference 경로 정리
- **중복 절** — 기본/품질 요구를 표로 통합해 길이 축소

레거시 Activities·작성자 정보는 그대로 두었습니다. PRD §7에 `D-LOC`/`U-IN`을 formalize하려면 `PRD.md`도 같이 맞출 수 있습니다.

[REDACTED]

---

## Turn 22 — user

<user_query>
PRD.md도 같이 맞춰줘.
</user_query>

---

## Turn 23 — assistant

[REDACTED]

[Tool: Read, Read]

---

## Turn 24 — assistant

PRD에 FR-LOC·FR-IN·D-LOC·U-IN을 반영하고, `reference.md`와 README 표기를 맞춥니다.

[REDACTED]

[Tool: StrReplace, StrReplace, StrReplace, StrReplace, StrReplace, StrReplace, StrReplace, StrReplace, StrReplace, Write, StrReplace, StrReplace, StrReplace]

---

## Turn 25 — assistant

`PRD.md`를 README·세션 계획과 맞춰 **v0.2.0**으로 갱신했습니다. 연동 파일도 함께 정리했습니다.

### PRD.md 주요 추가·변경

| 구분 | 내용 |
|------|------|
| **§2.3** | FR-LOC-01~03과 `constants` / `exceptions` / `BASE_UNIT` SSOT 연결 |
| **§3.5** | FR-LOC-01~03 (Location / SSOT) |
| **§3.6** | FR-IN-01~02 (boundary CLI 입력 표면화, FR-10/11과 쌍) |
| **§3.4** | UI TC는 메시지·exit assert 명시 |
| **§6.4** | 에러 입력 예시 (`meter:-2.5`, `meter2.5` 등) |
| **§7.1** | D-LOC-01~03 + Logic 묶음 표 |
| **§7.2** | U-IN-01~02 (M1 P0) + UI 묶음 표 |
| **§4** | NFR-10 (D-LOC), NFR-11 (U-IN) |
| **§8** | M1에 FR-LOC·FR-IN·U-IN 반영 |
| **§10** | 0.2.0 변경 이력 |

### 함께 맞춘 파일

- `.cursor/skills/unit-converter-tdd/reference.md` — D-LOC-01~03, U-* 목록
- `README.md` — “PRD 보강 예정” → §3.5/§3.6·§7.1/§7.2 참조
- `.cursor/commands/red-test-plan.md` — D-LOC·U-IN 묶음 참고

`LOC`는 **다국어가 아니라 SSOT 위치(Location)** 로 정의했습니다(§1.3 “다국어 UI 제외”와 충돌 없음).

[REDACTED]

---

## Turn 26 — user

<user_query>
아래 ECB dual-track TDD spec 단계 리뷰 내용을 참고해서 수정 진행해줘.

/review-ecb의 int[6] 1-index는 transcript에서도 불필요하다고 정리됐는데 Command에 남아 있습니다. ErrorCode Enum 체크로 바꾸거나 항목 제거를 권합니다.
MagicConstant SSOT: .cursorrules의 constants.py 또는 units.json → PRD대로 constants 단일 + JSON은 로드용으로 한 문장 통일. config/units.json 샘플 파일도 있으면 red가 수월합니다.
</user_query>

---

## Turn 27 — assistant

리뷰 반영을 위해 `/review-ecb`, `.cursorrules`, PRD, `config/` 현황을 확인합니다.

[REDACTED]

[Tool: Read, Read, Grep, Glob]

---

## Turn 28 — assistant

[REDACTED]

[Tool: Read, Read]

---

## Turn 29 — assistant

`review-ecb`의 `int[6]` 항목을 `ErrorCode` Enum 검사로 교체하고, `.cursorrules` SSOT 문구와 `config/units.json` 샘플을 추가합니다.

[REDACTED]

[Tool: Write, StrReplace, Write, StrReplace, Grep]

---

## Turn 30 — assistant

[REDACTED]

[Tool: Read, Grep]

---

## Turn 31 — assistant

[REDACTED]

[Tool: StrReplace, StrReplace, StrReplace]

---

## Turn 32 — assistant

spec 리뷰 반영을 마쳤습니다.

### 1. `/review-ecb` — `int[6]` 제거 → **ErrorCode Enum**
- 체크 **5항 → 4항**: import · **ErrorCode Enum (E001~E007)** · MagicConstant SSOT · Logic Mock
- `int[6]` 1-index는 **금지 레거시 패턴**으로만 명시(잔존 시 Warning)
- E001~**E007**로 PRD와 통일

### 2. `.cursorrules` — MagicConstant SSOT 한 문장
- **정본:** `entity/constants.py`만
- **`config/units.json`:** boundary 로드·주입용, JSON 수치를 코드·테스트에 리터럴 복사 금지

### 3. `config/units.json` 샘플 추가
- PRD §6.5와 동일 스키마 (`base_unit`, `units`, `precision`)
- RED/U-CFG-01에서 boundary 로드 경로로 바로 사용 가능

### 4. 기타 정합
| 파일 | 변경 |
|------|------|
| `README.md` | 구조에 `config/units.json` 명시 |
| `PRD.md` §6.5 | 샘플 파일 링크·SSOT 역할 문구 |
| `session-init.sh` | Enum SSOT·config 로드용·slash 커맨드 갱신 |

`SKILL.md`는 이미 `constants.py` 단일 SSOT라 수정하지 않았습니다. `Prompting/01-session-transcript.md`는 역사 기록이라 그대로 두었습니다.

[REDACTED]

---

## Turn 33 — user

<user_query>
Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘
</user_query>

---

## Turn 34 — assistant

Report·Prompting 폴더 구조와 기존 문서 형식을 확인한 뒤 보고서와 Transcript를 생성합니다.

[REDACTED]

[Tool: Read, Read, Read, Read]

---

## Turn 35 — assistant

`02-session-report.md` 작성, `02-session-transcript.md` jsonl Export, Report·Prompting README 인덱스 갱신 완료.

### 산출물

| 경로 | 설명 |
|------|------|
| `Report/02-session-report.md` | Spec 정합·RED 계획·SSOT 리뷰 종합 보고 |
| `Prompting/02-session-transcript.md` | 본 세션 대화 Export (34 turns + 마무리) |

---
