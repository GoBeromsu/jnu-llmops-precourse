"""records.py — 검색 규칙만 담는 Module. Day 3 에 app.py 에서 분리했다.

app.py 와 notebooks/analysis.ipynb 가 같은 find_records 를 import 해서 쓴다.
Signature 는 바꾸지 않는다: find_records(records, equipment_id, status)
"""

REQUIRED_KEYS = ("date", "equipment_id", "status")


# >>> TODO-GUIDED: D3-CHECK >>>
# Day 3: 기록에 없는 Key 를 꺼내다 실패하기 전에 먼저 확인하고, 무엇이 없는지 말해 준다.
def check_record(record, index):
    for key in REQUIRED_KEYS:
        if key not in record:
            raise KeyError(f"{index}번째 기록에 '{key}' 가 없습니다: {record}")
# <<< TODO-GUIDED: D3-CHECK <<<


# >>> TODO-GUIDED: D3-EXTRACT >>>
# Day 3: app.py 의 search 를 이 File 로 옮겼다. 이름은 find_records, 인자 순서는 고정.
def find_records(records, equipment_id, status):
    found = []
    for index, record in enumerate(records, start=1):
        check_record(record, index)
        if equipment_id != "ALL" and record["equipment_id"] != equipment_id:
            continue
        if status != "ALL" and record["status"] != status:
            continue
        found.append(record)
    return found
# <<< TODO-GUIDED: D3-EXTRACT <<<
