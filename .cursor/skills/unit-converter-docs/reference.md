# unit-converter-docs — Reference (SSOT: Report/08 · Prompting/08)

## Report 템플릿

```markdown
# NN — UnitConverter_07 [세션 주제] 세션 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_07 |
| 저장소 | https://github.com/msubkim-ship-it/UnitConverter_07 |
| 세션 일자 | YYYY-MM-DD |
| 브랜치 | `branch-name` |
| Phase | [RED|GREEN|REFACTOR|review|GUI Smoke|…] — [Layer] / [Track] |
| 대응 Transcript | [Prompting/NN-session-transcript.md](../Prompting/NN-session-transcript.md) |
| 작성 | AI Agent 세션 산출물 정리 |

---

## 1. 세션 목적

[NN-1] 세션 **…** 이후, …

- (불릿 3~5개)

---

## 2. 수행 작업 요약

| # | 주제 | 산출·결과 |
|---|------|-----------|
| 1 | … | … |
| … | Export | 본 보고서 + `NN-session-transcript.md` |

---

## 3. 추가·변경 파일

| 파일 | Layer | 역할 |
|------|-------|------|
| … | entity|control|boundary|— | … |

**미커밋:** (해당 시 working tree 명시)

---

## 4. ECB 아키텍처

```text
boundary/… → control/… → entity/…
```

| 점검 | 결과 |
|------|------|
| import 방향 | ✅ / ❌ |
| MagicConstant SSOT | ✅ / ⚠️ |
| ErrorCode Enum | ✅ / ⚠️ |

---

## 5. [기능·주제별 섹션]

(08 예: GUI 스모크 테스트 기능 — 화면·실행·수동 시나리오)

---

## 6. pytest·변환 검증

| 명령 | exit | 결과 |
|------|------|------|
| `python -m pytest tests/ -v` | **0** / **1** | N passed / failed |

**판정:** …

---

## 7. [환경·이슈] (해당 시)

---

## 8. PRD·TDD 대비

| FR/NFR | 반영 | TDD 상태 |
|--------|------|----------|
| FR-01 | ✅ / ⚠️ | D-* / U-* |

---

## 9. ARRR·루프 조사 (해당 시)

| 질문 | 답 |
|------|-----|
| … | … |

---

## 10. 미완·다음 단계

| 우선순위 | 항목 |
|:--:|------|
| P0 | … |
| P1 | … |

---

## 11. AI 활용 회고

| 도움이 된 점 | 한계 |
|-------------|------|
| … | … |

---

## 12. 관련 링크

- 이전 보고: [NN-1-session-report.md](./NN-1-session-report.md)
- Transcript: [../Prompting/NN-session-transcript.md](../Prompting/NN-session-transcript.md)
- Source: `agent-transcripts/<uuid>.jsonl`

---

작성자: 김명섭  
리뷰어: 김민주, 김소민, 김연우, 김정균, 김준호
```

---

## Transcript 템플릿

```markdown
# NN — UnitConverter_07 Session Transcript
> Source: agent-transcripts/<uuid>.jsonl
> Exported: YYYY-MM-DD

---

## Turn 1 — user

<user_query>
…
</user_query>

---

## Turn 2 — assistant

[한 줄 요약]

[REDACTED]

[Tool: Grep …, Read …, Shell pytest …]

| 항목 | 결과 |
|------|------|
| … | … |

---

*End of transcript (N turns)*
```

### Transcript 축약 규칙

| 유형 | 처리 |
|------|------|
| 연속 tool call | `[Tool: Read X, Write Y, Shell Z]` 한 줄 |
| 긴 코드 diff | 표 또는 파일 경로만 |
| 동일 주제 반복 | 마지막 결과 표만 |
| cursor_commands | Turn 1에 `<cursor_commands>` 블록 유지 가능 |

---

## README 인덱스 행

### Report/README.md

```markdown
| NN | [NN-session-report.md](./NN-session-report.md) | [한 줄 설명] | [NN-session-transcript.md](../Prompting/NN-session-transcript.md) |
```

### Prompting/README.md

```markdown
| NN | [NN-session-transcript.md](./NN-session-transcript.md) | [한 줄 설명] (N turns) | [NN-session-report.md](../Report/NN-session-report.md) |
```

하단 Source 주석:

```markdown
> NN Source: `agent-transcripts/<uuid>.jsonl`
```

(분할 Export 시: `(Turn X~)` 또는 `(Turn X~)` 표기 — 05·07 참고)

---

## Phase ARRR 체크리스트 (1사이클)

```
Task Progress — Session NN Export:
- [ ] A1 세션 번호 NN 확정
- [ ] A2 git·변경 파일·커밋
- [ ] A3 pytest (해당 시)
- [ ] A4 transcript source·turn 수
- [ ] R1 Report/NN-session-report.md
- [ ] R2 Prompting/NN-session-transcript.md
- [ ] R3 §10·§11·§12 + README 인덱스
```
