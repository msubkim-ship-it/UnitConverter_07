# 08 — UnitConverter_07 GUI 스모크 테스트 세션 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_07 |
| 저장소 | https://github.com/msubkim-ship-it/UnitConverter_07 |
| 세션 일자 | 2026-06-05 |
| 브랜치 | `refactoring` |
| Phase | GUI Smoke Test — boundary / UI Track (수동 확인용) |
| 대응 Transcript | [Prompting/08-session-transcript.md](../Prompting/08-session-transcript.md) |
| 작성 | AI Agent 세션 산출물 정리 |

---

## 1. 세션 목적

07 세션 **REFACTOR Safe·리뷰 반영** 이후, 지금까지의 구현 결과(D-LOC-01 SSOT·기본 변환)를 **REPL/CLI 대신 GUI**로 빠르게 확인할 수 있는 **스모크 테스트 하네스**를 추가한다.

- REPL 스모크 테스트 개념 설명 (질의 응답)
- PyQt6/PySide6 기반 boundary GUI 구현
- ECB 준수: `boundary → control → entity`
- pytest Logic Track(D-LOC-01) **PASS 유지**
- ARRR 전용 질문지 유무 조사 (본 저장소에는 없음 — Test/Review Loop로 대체)

---

## 2. 수행 작업 요약

| # | 주제 | 산출·결과 |
|---|------|-----------|
| 1 | REPL 스모크 테스트 설명 | 프로젝트 내 공식 용어 없음 — pytest vs 수동 sanity check 구분 |
| 2 | `entity/constants.py` 확장 | `BASE_UNIT`, `DEFAULT_UNITS`, `UNIT_RATIOS` 추가 |
| 3 | `control/conversion_service.py` 신규 | `parse_unit_value`, `convert_all`, `convert_from_text` |
| 4 | `boundary/gui_smoke.py` 신규 | Qt GUI — SSOT 표시·입력·변환·오류 표면화 |
| 5 | `run_gui_smoke.py` 런처 | `pythonpath=src` 주입 후 GUI 실행 |
| 6 | `pyproject.toml` | optional `[gui]` — `PySide6>=6.6` |
| 7 | Qt 바인딩 | PyQt6 SSL 실패 → **PySide6** 설치·동작 (PyQt6/PySide6 자동 선택) |
| 8 | ARRR 조사 | _07에 ARRR 질문지 없음 — Skill·Commands·Report §5가 유사 루프 |
| 9 | Export | 본 보고서 + `08-session-transcript.md` |

---

## 3. 추가·변경 파일

| 파일 | Layer | 역할 |
|------|-------|------|
| `src/entity/constants.py` | entity | SSOT 확장 (`BASE_UNIT`, `UNIT_RATIOS` 등) |
| `src/control/conversion_service.py` | control | 변환 유스케이스·입력 검증(스모크 수준) |
| `src/boundary/gui_smoke.py` | boundary | PyQt6/PySide6 GUI 스모크 창 |
| `run_gui_smoke.py` | — | GUI 실행 진입점 |
| `pyproject.toml` | Harness | `[project.optional-dependencies] gui = ["PySide6>=6.6"]` |

**미커밋:** 위 파일 전부 working tree (본 세션 종료 시).

---

## 4. ECB 아키텍처

```text
boundary/gui_smoke.py
    → control/conversion_service.py
        → entity/constants.py, entity/loc.py
```

| 점검 | 결과 |
|------|------|
| import 방향 | ✅ boundary → control → entity |
| MagicConstant SSOT | ✅ 비율은 `constants.py`만 참조 |
| entity I/O | ✅ entity에 GUI·control import 없음 |
| ErrorCode Enum | ⚠️ `ConversionError`(임시) — D-LOC-02 `exceptions.py` 도입 전 |

---

## 5. GUI 스모크 테스트 기능

### 5.1 화면 구성

| 영역 | 확인 항목 |
|------|-----------|
| SSOT 패널 | D-LOC-01 G1 row-major 비율, 등록 단위 테이블 |
| 입력 패널 | `단위:값` 텍스트, 단위 콤보 + 숫자, 콤보→텍스트 동기화 |
| 결과 패널 | FR-02·FR-04 — 입력 단위 제외, 소수 1자리 |
| 오류 | 형식 오류, 음수, 미등록 단위 — QMessageBox + 결과창 |

### 5.2 실행 방법

```powershell
pip install -e ".[gui]"
# 또는: pip install PySide6

python run_gui_smoke.py
```

### 5.3 수동 스모크 시나리오 (권장)

| # | 입력 | 기대 결과 |
|---|------|-----------|
| 1 | `meter:2.5` | `2.5 meter = 8.2 feet`, `2.5 meter = 2.7 yard` |
| 2 | `feet:3.28084` | meter ≈ 1.0 |
| 3 | `meter2.5` | 형식 오류 메시지 |
| 4 | `meter:-1` | 음수 거부 |
| 5 | `cubit:1` | 미등록 단위 |

---

## 6. pytest·변환 검증

| 명령 | exit | 결과 |
|------|------|------|
| `python -m pytest tests/ -v` | **0** | **1 passed** (`test_d_loc_01`) |
| `convert_from_text('meter:2.5')` | — | `['2.5 meter = 8.2 feet', '2.5 meter = 2.7 yard']` |
| GUI import (`SmokeTestWindow`) | — | **OK** (PySide6) |

**판정:** Logic Track TC 동결 — D-LOC-01 GREEN 유지. GUI는 **U-* TC·Golden Master 범위 밖**(수동 스모크).

---

## 7. PyQt6 vs PySide6

| 항목 | 내용 |
|------|------|
| PyQt6 `pip install` | SSL `CERTIFICATE_VERIFY_FAILED` — 설치 실패 |
| PySide6 | `--trusted-host`로 설치 성공 |
| 코드 | PyQt6 우선 import → 실패 시 PySide6 fallback |
| 창 제목 | `GUI Smoke Test (PySide6)` 등 바인딩명 표시 |

---

## 8. PRD·TDD 대비

| FR/NFR | GUI 반영 | TDD 상태 |
|--------|----------|----------|
| FR-01 `단위:값` | ✅ control 파싱 | U-* TC 없음 |
| FR-02 다른 단위 변환 | ✅ 입력 단위 제외 | D-CONV-* 미착수 |
| FR-04 소수 1자리 | ✅ `:.1f` | — |
| FR-10~12 검증 | ⚠️ 메시지 문자열 (E001~E007 Enum 전) | D-LOC-02 미착수 |
| NFR-04 테스트 가능 | ✅ control은 pytest 가능 (TC 미작성) | — |

**범위:** 스모크·데모용 최소 구현 — **GREEN Phase 공식 U-* TC·Golden은 후속**.

---

## 9. ARRR 조사 요약

| 질문 | 답 |
|------|-----|
| _07에 ARRR 질문지? | **없음** |
| 대체 루프 | Test/Review Loop 5항, Slash Commands, Skill 완료 보고 8항 |
| 형제 프로젝트 | UnitConverter_1004 — `unit-converter-arr-cycle` Skill·WORKBOOK |

---

## 10. 미완·다음 단계

| 우선순위 | 항목 |
|:--:|------|
| P0 | 스모크 GUI 변경사항 **commit** (사용자 요청 시) |
| P1 | README — GUI 스모크 실행 절 추가 |
| P1 | `/red-skeleton` — D-CONV-01~06, D-LOC-02 |
| P2 | `exceptions.py` SSOT + GUI `ErrorCode` 연동 |
| P2 | U-CLI-01 RED → boundary pytest (GUI 대체 아님) |
| P3 | ARRR 질문지 _07 이식 또는 Test/Review Loop 템플릿화 |

---

## 11. AI 활용 회고

| 도움이 된 점 | 한계 |
|-------------|------|
| D-LOC-01 SSOT를 GUI 패널로 시각화 — 스모크 가치 명확 | TDD RED/GREEN 없이 control·boundary 추가 — 공식 TC 추적 없음 |
| PyQt6 SSL 실패 시 PySide6 fallback — Windows 환경 대응 | `ConversionError`가 E001~E007 계약과 아직 불일치 |
| ECB 단방향 유지하며 레거시 `UnitConverter.py` 로직 이관 | GUI 자동 테스트(U-*)·Golden Master 미연동 |

---

## 12. 관련 링크

- 이전 보고: [07-session-report.md](./07-session-report.md)
- Transcript: [../Prompting/08-session-transcript.md](../Prompting/08-session-transcript.md)
- Source: `agent-transcripts/ab6c1f8c-0708-44b3-90c2-b83dcea25105.jsonl`

---

작성자: 김명섭  
리뷰어: 김민주, 김소민, 김연우, 김정균, 김준호
