# REFACTOR Smell — 코드 스멜 진단 (수정 금지)

GREEN 통과 후 `src/`의 **레거시 스멜·ECB 위반**을 표로만 진단한다.  
**다음:** `/refactor-safe`에서 선택 항목만 수정. `/review-ecb`와 병행 가능.

## 필수 선언

```
Phase: refactor-smell | Layer: all | Track: —
```

## 절차

1. **브랜치** — `refactoring` 권장 (green에서도 읽기 전용 진단 가능).
2. **스캔** — `src/entity/`, `src/control/`, `src/boundary/`, `UnitConverter.py`
3. **진단 항목**

| 카테고리 | 스멜 예시 (UnitConverter) |
|----------|---------------------------|
| SRP | Parser+Validator+Convert 한 클래스 |
| OCP | `if-elif` 단위 분기 |
| ECB | entity가 control import |
| SSOT | `3.28084` 리터럴 산재 |
| DRY | meter 환산 in/out 중복 |
| God | `main()`에 I/O+도메인 혼재 |
| 레거시 | `UnitConverter.py` domain 로직 잔존 |

4. **PRD·스멜 대조** — [초기 레거시 분석](../../README.md) 대비 개선·잔존.
5. **표 출력** — 수정 제안 1줄, **파일 수정 금지**.

## 출력 표

| # | 스멜 | 심각도 | 파일:줄 | 설명 | refactor-safe 권고 |
|---|------|--------|---------|------|-------------------|
| 1 | Magic Number | Warning | `src/control/...` | constants 미참조 | entity SSOT 이동 |

- 스멜 0건 → `PASS`
- 심각도: Critical(ECB 역방향) / Warning(SSOT·DRY)

## 보고

| 항목 | 내용 |
|------|------|
| 스멜 건수 | Critical / Warning |
| 우선 refactor | 1~3건 ID |
| 다음 | `/refactor-safe` 대상 |

## 금지

- `src/`, `tests/`, `golden/` **수정**
- pytest로 green 깨뜨리는 변경
- **git commit** (사용자 요청 없이)
