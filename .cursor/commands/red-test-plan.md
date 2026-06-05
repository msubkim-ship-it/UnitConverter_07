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
| SSOT 위치 | D-LOC-01 ~ 03 |

### UI Track (U-*) 참고 — [PRD §7.2](../../PRD.md)

`U-IN-01`, `U-IN-02`, `U-CLI-01`, `U-FMT-01/02`, `U-CFG-01`, `U-REG-01`

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
