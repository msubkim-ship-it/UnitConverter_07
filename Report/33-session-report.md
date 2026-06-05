# 33 — UnitConverter_07 GUI 스모크 테스트 갱신 세션 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_07 |
| 저장소 | https://github.com/msubkim-ship-it/UnitConverter_07 |
| 세션 일자 | 2026-06-05 |
| 브랜치 | `refactoring` |
| Phase | GUI Smoke Test — boundary / UI Track (수동 확인용) |
| 대응 Transcript | [Prompting/33-session-transcript.md](../Prompting/33-session-transcript.md) |
| 작성 | AI Agent 세션 산출물 정리 |

---

## 1. 세션 목적

32 세션 **U-REG-01 GREEN·pytest 29 passed** 이후, 08 세션에서 추가된 GUI 스모크 하네스가 **D-LOC·D-ERR·D-REG·U-* GREEN** 상태와 불일치하므로, 현재 ECB 스택에 맞게 **boundary `gui_smoke.py`를 갱신**한다.

- `UnitRegistry` 기반 동적 단위·변환 (FR-08, D-REG-01)
- ErrorCode SSOT(E001~E007) + `message_for` 표면화 (FR-LOC-02, D-ERR-*)
- 출력 포맷 table / json / csv (FR-09, U-FMT-*)
- pytest Logic·UI Track **29 passed 유지**
- Export — 본 보고서 + Transcript + git commit/push

---

## 2. 수행 작업 요약

| # | 주제 | 산출·결과 |
|---|------|-----------|
| 1 | 프로젝트·기존 GUI 조사 | `gui_smoke.py`, control/boundary/entity SSOT 대조 |
| 2 | `gui_smoke.py` 갱신 | UnitRegistry·등록 패널·포맷 콤보·ErrorCode 표시 |
| 3 | 변환 경로 교체 | `convert_from_text()` → `convert_all(..., ratios=, units=)` |
| 4 | pytest | `python -m pytest tests/ -q` exit **0**, **29 passed** |
| 5 | GUI import | PySide6 설치 후 `SmokeTestWindow` import **OK** |
| 6 | 등록·변환 수동 검증 | cubit 등록 후 `meter:2.5` → feet·yard·cubit 3줄 |
| 7 | Export | 본 보고서 + `33-session-transcript.md` + commit/push |

---

## 3. 추가·변경 파일

| 파일 | Layer | 역할 |
|------|-------|------|
| `src/boundary/gui_smoke.py` | boundary | 스모크 GUI — Registry·등록·포맷·E00x 표면화 |
| `Report/33-session-report.md` | — | 세션 보고서 |
| `Prompting/33-session-transcript.md` | — | Transcript Export |
| `Report/README.md` | — | 인덱스 33행 추가 |
| `Prompting/README.md` | — | 인덱스 33행 추가 |

---

## 4. ECB 아키텍처

```text
boundary/gui_smoke.py
    → boundary/error_messages.py
    → control/conversion_service.py, control/unit_registry.py
        → entity/constants.py, entity/exceptions.py, entity/loc.py
```

| 점검 | 결과 |
|------|------|
| import 방향 | ✅ boundary → control → entity |
| MagicConstant SSOT | ✅ 비율은 `constants.py`만 참조 |
| ErrorCode Enum | ✅ `exceptions.py` SSOT + `message_for` |
| entity I/O | ✅ entity에 GUI import 없음 |

---

## 5. GUI 스모크 테스트 기능 (갱신)

### 5.1 화면 구성

| 영역 | 확인 항목 |
|------|-----------|
| SSOT 패널 | G1 row-major, ErrorCode E001~E007, UnitRegistry 단위 테이블 |
| 등록 패널 | FR-08 `1 cubit = 0.4572 meter`, 샘플 입력 버튼 |
| 입력 패널 | `단위:값`, 콤보·숫자, **table/json/csv** 포맷 |
| 결과 패널 | FR-02·FR-04 변환 출력 |
| 오류 | `[E00x] 메시지` + QMessageBox + 상태줄 |

### 5.2 실행 방법

```powershell
pip install -e ".[gui]"
python run_gui_smoke.py
```

### 5.3 수동 스모크 시나리오 (권장)

| # | 동작 | 기대 결과 |
|---|------|-----------|
| 1 | `meter:2.5` (table) | feet·yard 2줄 |
| 2 | 등록 `1 cubit = 0.4572 meter` | cubit 단위 테이블·콤보 추가 |
| 3 | 등록 후 `meter:2.5` | cubit 포함 3줄 |
| 4 | `meter2.5` | `[E001]` 형식 오류 |
| 5 | `meter:-1` | `[E003]` 음수 거부 |
| 6 | cubit 중복 등록 | `[E007]` 중복 거부 |
| 7 | json / csv 포맷 | U-FMT와 동일 구조 |

---

## 6. pytest·변환 검증

| 명령 | exit | 결과 |
|------|------|------|
| `python -m pytest tests/ -q` | **0** | **29 passed** |
| Registry + `meter:2.5` (스크립트) | — | feet·yard·cubit 3줄 |
| GUI import (`SmokeTestWindow`) | — | **OK** (PySide6) |

**판정:** 공식 TC 동결 — Logic 17 + UI 7 GREEN 유지. GUI는 **U-* TC·Golden 범위 밖**(수동 스모크).

---

## 8. PRD·TDD 대비

| FR/NFR | GUI 반영 | TDD 상태 |
|--------|----------|----------|
| FR-01 `단위:값` | ✅ | D-* / U-CLI GREEN |
| FR-02·FR-04 변환·포맷 | ✅ | D-CONV-* / U-CLI GREEN |
| FR-08 동적 등록 | ✅ Registry 패널 | D-REG-01 / U-REG-01 GREEN |
| FR-09 JSON/CSV/표 | ✅ 포맷 콤보 | U-FMT-01~02 GREEN |
| FR-10~15·E001~E007 | ✅ ErrorCode 표면화 | D-ERR-* / U-IN-* GREEN |
| FR-LOC-01~03 | ✅ SSOT 패널 | D-LOC-* GREEN |
| NFR-03 ECB | ✅ | import 역방향 없음 |

**범위:** 스모크·데모용 — 공식 U-* 자동 TC 추가 없음.

---

## 10. 미완·다음 단계

| 우선순위 | 항목 |
|:--:|------|
| P1 | README — GUI 스모크 실행 절·수동 시나리오 추가 |
| P2 | CLI `run_cli` 변환 경로에 Registry 연동 (GUI와 동일 gap) |
| P2 | `config/units.json` 로드 — GUI config 패널 (U-CFG-01) |
| P3 | staging merge·PR 정리 |

---

## 11. AI 활용 회고

| 도움이 된 점 | 한계 |
|-------------|------|
| 08 GUI와 32세션 ECB 스택 diff 대조로 갱신 범위 명확 | GUI 자동 pytest(U-*) 미작성 — 수동 스모크만 |
| UnitRegistry + convert_all로 등록 후 변환 end-to-end 검증 | formatter.py는 Registry 미지원 — GUI에 json/csv 인라인 |
| pytest 29 passed 유지로 TDD 게이트 무손상 확인 | README 본문 GUI 절은 후속(P1) |

---

## 12. 관련 링크

- 이전 보고: [32-session-report.md](./32-session-report.md)
- Transcript: [../Prompting/33-session-transcript.md](../Prompting/33-session-transcript.md)
- Source: `agent-transcripts/192bf137-24ff-454f-9eb1-5018a6ac2ded.jsonl`

---

작성자: 김명섭  
리뷰어: 김민주, 김소민, 김연우, 김정균, 김준호
