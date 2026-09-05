# jnu-llmops-precourse — Virtual Lab Records

전남대학교 LLM Ops 사전 강의 (2026-09-07 ~ 09-10, 매일 17:00–20:00) 실습 저장소.
가상 실험실의 장비 점검 기록 12 건을 검색해 출력하는 작은 CLI Program 하나를 4 일 동안 함께 키운다.
Upstage LLMOps 본과정에서 Python Code 와 환경 때문에 막히지 않도록, 실행·Data Flow·오류 복구·변경 관리의 기초를 몸으로 익히는 것이 목표다.

이 저장소에는 실습 File 만 있다. 슬라이드와 강의안은 수업에서 따로 받는다.

## 수업 전 준비 (Readiness check)

| 항목 | 확인 방법 | 기준 |
| --- | --- | --- |
| Python | `python3 --version` (Windows: `py -3 --version`) | 3.11 이상 |
| Git | `git --version` | 어떤 버전이든 설치되어 있으면 된다 |
| Editor | VS Code + Python + Jupyter 확장, 또는 `jupyter lab` 실행 가능 | Notebook 은 Day 4 에만 쓴다 |
| GitHub | Browser Login 이 되고, 개인 Branch 를 Push 할 수 있다 | Push 가 안 되면 조교에게 미리 말한다 |
| 이 저장소 | `git clone https://github.com/GoBeromsu/jnu-llmops-precourse.git` 후 `cd jnu-llmops-precourse` | Clone 이 되어야 Day 1 실습을 시작할 수 있다 |

한 번에 확인:

```sh
python3 scripts/check.py ENV        # Windows: py -3 scripts/check.py ENV
```

`[PASS] ENV` 가 나온 Interpreter 를 수업 내내 그대로 쓴다.

## 실행 방법

모든 명령은 **저장소 Root** 에서 실행한다. macOS/Linux 는 `python3`, Windows 는 `py -3`.

```sh
python3 app.py                              # Program 실행
python3 scripts/check.py <BLOCK-ID>         # 실습 Block 확인
python3 scripts/reset_checkpoint.py <BLOCK-ID>   # 예정된 실패에서 복구
```

## 4 일의 흐름

| Day | 그날 저장소에 있는 File | 실습 Block | 한 줄 요약 |
| --- | --- | --- | --- |
| 1 | `app.py` | `D1-FMT` | 출력 Formatting 을 바꾸고 첫 Commit, 개인 Branch |
| 2 | `app.py` | `D2-TARGET` | 검색할 장비를 바꿔 결과가 달라지는 것을 본다 |
| 3 | `app.py` + `records.py` + `experiment_records.json` | `D3-FILTER` `D3-EXTRACT` `D3-JSON` `D3-CHECK` | 조건을 좁히고, 검색을 Module 로 나누고, Data 를 File 로 분리하고, 없는 Key 를 확인한다 |
| 4 | 위 세 File + `notebooks/analysis.ipynb` | `D4-IMPORT` | Notebook 이 같은 Module 을 import 해 같은 숫자를 낸다. Push 와 개인 Pull Request |

`records.py` 와 `experiment_records.json` 은 Day 1 Clone 에 **없다**. Day 3 에 여러분이 만든다.
`notebooks/analysis.ipynb` 는 Day 1 부터 들어 있지만 **Day 4 에 연다**.

## TODO-GUIDED Block

여러분이 고치는 범위는 아래 마커 사이 **5~15 줄**로 제한된다. 마커 밖은 읽기만 한다.

```python
# >>> TODO-GUIDED: D1-FMT >>>
... 여러분이 고치는 줄 (마커 사이 5~15 줄) ...
# <<< TODO-GUIDED: D1-FMT <<<
```

Block ID (Block 마다 하나, 날짜마다가 아니다): `D1-FMT` `D2-TARGET` `D3-FILTER` `D3-EXTRACT` `D3-JSON` `D3-CHECK` `D4-IMPORT`
복구 전용 ID: `DAY4-START` (Day 4 시작 전 전원을 Day 3 완성 상태로 맞춘다)

## 정합표 (Reconciliation table)

슬라이드·강의안·실습 지도안은 이 표를 그대로 복사한다. 이 표가 기준이다.

| day | files present that day | repo path | symbol | block id | marker line range | edit-size rule | run CWD | canonical invocation | checker assertion | expected stdout (pre / instructor-reference) | checkpoint semantics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `app.py` `pyproject.toml` `README.md` `notebooks/analysis.ipynb` `scripts/*` `checkpoints/*` | — | layout | — | — | — | repo root | `python3 app.py` / `py -3 app.py` | — | pre: 14 줄 (머리 2 + 기록 12) | — |
| 1 | `app.py` | `app.py` | `HEADER_TITLE` `HEADER_RULE` `COLUMN_SEP` `LABEL_DATE` `LABEL_EQUIPMENT` `LABEL_STATUS` | `D1-FMT` | 34–42 (사이 7 줄) | 5~8 줄, 따옴표 안 문자열만 | repo root | `python3 scripts/check.py D1-FMT` | 출력 14 줄, 기록 12 건에 HPLC-01 8·Warning 2, Block 이 시작 상태와 다름. 모양은 보지 않는다 | pre: 아래 §pre-edit / instructor-reference: 아래 §reference (non-asserting) | `git restore app.py` 와 같음 — Commit 되지 않은 변경만 버린다. Commit 은 남는다 |
| 2 | `app.py` (Day 1 과 같음) | — | layout | — | — | — | repo root | `python3 app.py` | — | `HPLC-01` 로 좁히면 10 줄 (머리 2 + 8) | — |
| 2 | `app.py` | `app.py` | `target_equipment` `target_status` | `D2-TARGET` | 26–32 (사이 5 줄) | 5~8 줄, 따옴표 안 문자열만 | repo root | `python3 scripts/check.py D2-TARGET` | 결과가 0 건도 12 건도 아님 | pre: 14 줄 / 정본: 10 줄 | `checkpoints/D2-TARGET/app.py` 를 덮어쓰고 Stage 하지 않음 |
| 3 | `app.py` `records.py` `experiment_records.json` | — | layout | — | — | — | repo root | `python3 app.py` | — | Warning 만 남기면 4 줄 (머리 2 + 2) | — |
| 3 | `app.py` | `app.py` | `search` 안의 `for`/`if` | `D3-FILTER` | 48–54 (사이 5 줄) | 5~10 줄 | repo root | `python3 scripts/check.py D3-FILTER` | Block 에 `status` 조건, 결과 2 건 | 4 줄 | `checkpoints/D3-FILTER/app.py` |
| 3 | `records.py` (새 File) | `records.py` | `find_records(records, equipment_id, status)` | `D3-EXTRACT` | 8–19 (사이 10 줄) | 8~15 줄 | repo root | `python3 scripts/check.py D3-EXTRACT` | `records.py` 존재, `RecordPrinter` 는 `app.py` 에, `app.py` 가 import, 옛 `search` 삭제, 8 건/2 건/빈 List | 분리 전후 같은 4 줄 | `checkpoints/D3-EXTRACT/{app.py,records.py}` |
| 3 | `experiment_records.json` (새 File) | `app.py` | `RECORDS_PATH` `json.load` | `D3-JSON` | 14–20 (사이 5 줄) | 5~10 줄 | repo root (`notebooks/` 에서는 실패) | `python3 scripts/check.py D3-JSON` | JSON File 존재, Code 안 List 삭제, 12/8/2 유지 | 같은 4 줄 | `checkpoints/D3-JSON/{app.py,records.py,experiment_records.json}` |
| 3 | `records.py` | `records.py` | `check_record` `REQUIRED_KEYS` | `D3-CHECK` | 10–16 (사이 5 줄) | 5~10 줄, 광범위한 `try/except` 금지 | repo root | `python3 scripts/check.py D3-CHECK` | `status` 없는 기록에 이름을 말하는 `KeyError`, 정상 기록은 2 건 | 같은 4 줄 | `checkpoints/D3-CHECK/*` |
| 4 | 위 세 File + `notebooks/analysis.ipynb` | — | layout | `DAY4-START` | — | — | repo root (Notebook 도 Root 기준) | `python3 scripts/reset_checkpoint.py DAY4-START` | — | — | 전원을 Day 3 완성 상태로 맞춘다 |
| 4 | `notebooks/analysis.ipynb` | `notebooks/analysis.ipynb` | `find_warnings` → `from records import find_records` | `D4-IMPORT` | Code Cell 기준 10–21 (사이 10 줄) | 5~10 줄 | repo root | `python3 scripts/check.py D4-IMPORT` | 복사 Loop 삭제, import 존재, 장비별 Warning 2/0/0 = CLI 와 일치 | Notebook 출력 `{'HPLC-01': 2, 'GC-02': 0, 'CENT-03': 0}` | `checkpoints/D4-IMPORT/analysis.ipynb` → `notebooks/analysis.ipynb` |

## 기대 출력

### pre-edit (Day 1 Clone 직후, 검사 기준)

정확히 14 줄. 머리 2 줄 + 기록 12 줄. 꼬리 줄 없음.

```
장비 점검 기록
----------------------------
날짜 2026-08-03 | 장비 HPLC-01 | 상태 OK
날짜 2026-08-04 | 장비 HPLC-01 | 상태 OK
날짜 2026-08-05 | 장비 GC-02 | 상태 OK
날짜 2026-08-06 | 장비 HPLC-01 | 상태 Warning
날짜 2026-08-07 | 장비 HPLC-01 | 상태 OK
날짜 2026-08-10 | 장비 CENT-03 | 상태 OK
날짜 2026-08-11 | 장비 HPLC-01 | 상태 OK
날짜 2026-08-12 | 장비 HPLC-01 | 상태 Warning
날짜 2026-08-13 | 장비 GC-02 | 상태 OK
날짜 2026-08-14 | 장비 HPLC-01 | 상태 OK
날짜 2026-08-17 | 장비 CENT-03 | 상태 OK
날짜 2026-08-18 | 장비 HPLC-01 | 상태 OK
```

### instructor-reference (강사 예시, **non-asserting**)

강사가 슬라이드에 쓰는 예시 편집이다. 검사는 이 모양을 **요구하지 않는다** — 여러분은 자유롭게 바꿔도 된다.
예: `COLUMN_SEP = "  ·  "`, `LABEL_STATUS = "결과"` 로 바꾸면

```
장비 점검 기록
----------------------------
날짜 2026-08-03  ·  장비 HPLC-01  ·  결과 OK
... (12 줄)
```

## 복구 (Checkpoint)

예정된 실패는 수업의 일부다. 실패하면 먼저 `git diff` 와 Traceback 을 읽고, 그 다음 되돌린다.

| BLOCK-ID | 되돌리는 것 | 남는 것 |
| --- | --- | --- |
| `D1-FMT` | `app.py` 의 Commit 되지 않은 변경 | 여러분의 Commit |
| `D2-TARGET` `D3-FILTER` `D3-EXTRACT` `D3-JSON` `D3-CHECK` | 해당 File 을 `checkpoints/<ID>/` 정본으로 덮어쓴다 (Stage 하지 않음) | 덮어쓴 File 을 `git diff` 로 읽고 Commit 하는 것은 여러분 몫 |
| `DAY4-START` | 세 File 을 Day 3 완성 상태로 | — |
| `D4-IMPORT` | `notebooks/analysis.ipynb` | — |

모르는 ID 를 넣으면 `[FAIL]` 과 함께 가능한 ID 목록이 나온다.

## Day 4 Notebook 실행 위치

Notebook 은 저장소 Root 기준으로 `records.py` 와 `experiment_records.json` 을 찾는다.
VS Code 는 `.vscode/settings.json` 의 `jupyter.notebookFileRoot` 가 Root 를 잡아 준다. `jupyter lab` 은 Root 에서 실행한다. 첫 Code Cell 이 Root 를 한 번 더 확인한다.

## Push 가 안 될 때

GitHub 인증이 안 되면 Local 에서 Commit 까지 하고, 강사가 미리 열어 둔 읽기용 PR 을 보며 같은 구조로 자기 PR 본문을 씁니다: [강사 예시 PR](https://github.com/GoBeromsu/jnu-llmops-precourse/pull/1)
