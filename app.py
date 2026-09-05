"""Virtual Lab Records — 장비 점검 기록을 검색해서 출력하는 작은 CLI Program.

Day 1: 출력 Formatting 을 바꾸고 첫 Commit 을 남긴다 (D1-FMT).
Day 2: 검색할 장비를 바꿔 결과가 달라지는 것을 확인한다 (D2-TARGET).
Day 3: 조건을 좁히고 (D3-FILTER), 검색을 records.py 로 옮기고 (D3-EXTRACT),
       기록을 JSON File 로 분리하고 (D3-JSON), 없는 Key 를 확인한다 (D3-CHECK).
실행: 저장소 Root 에서  python3 app.py   (Windows: py -3 app.py)
"""

import json

from records import find_records

# >>> TODO-GUIDED: D3-JSON >>>
# Day 3: Code 안에 박혀 있던 기록을 외부 JSON File 에서 읽는다.
# 경로는 실행 위치(저장소 Root) 기준이다. notebooks/ 에서 실행하면 찾지 못한다.
RECORDS_PATH = "experiment_records.json"
with open(RECORDS_PATH, encoding="utf-8") as f:
    RECORDS = json.load(f)
# <<< TODO-GUIDED: D3-JSON <<<

# >>> TODO-GUIDED: D2-TARGET >>>
# Day 2: 검색할 장비를 바꿔 본다. 따옴표 안의 문자열만 바꾼다.
# 장비 ID 후보: "HPLC-01", "GC-02", "CENT-03"
# "ALL" 은 장비로 걸러내지 않고 12 건을 모두 보여 준다.
target_equipment = "HPLC-01"
target_status = "Warning"
# <<< TODO-GUIDED: D2-TARGET <<<

# >>> TODO-GUIDED: D1-FMT >>>
# Day 1: 출력 모양을 바꿔 본다. 따옴표 안의 문자열만 바꾼다.
HEADER_TITLE = "장비 점검 기록"
HEADER_RULE = "----------------------------"
COLUMN_SEP = "  ·  "
LABEL_DATE = "날짜"
LABEL_EQUIPMENT = "장비"
LABEL_STATUS = "결과"
# <<< TODO-GUIDED: D1-FMT <<<


class RecordPrinter:
    """기록 한 건을 사람이 읽는 한 줄로 바꾼다. Class 는 읽기만 한다. 수정하지 않는다."""

    def to_line(self, record):
        return (
            f"{LABEL_DATE} {record['date']}"
            f"{COLUMN_SEP}{LABEL_EQUIPMENT} {record['equipment_id']}"
            f"{COLUMN_SEP}{LABEL_STATUS} {record['status']}"
        )

    def print_all(self, records):
        print(HEADER_TITLE)
        print(HEADER_RULE)
        for record in records:
            print(self.to_line(record))


def main():
    found = find_records(RECORDS, target_equipment, target_status)
    printer = RecordPrinter()
    printer.print_all(found)


if __name__ == "__main__":
    main()
