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
