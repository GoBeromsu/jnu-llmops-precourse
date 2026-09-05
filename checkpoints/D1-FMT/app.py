"""Virtual Lab Records — 장비 점검 기록을 검색해서 출력하는 작은 CLI Program.

Day 1: 출력 Formatting 을 바꾸고 첫 Commit 을 남긴다 (D1-FMT).
Day 2: 검색할 장비를 바꿔 결과가 달라지는 것을 확인한다 (D2-TARGET).
Day 3: 조건을 좁히고 (D3-FILTER), 검색을 records.py 로 옮기고 (D3-EXTRACT),
       기록을 JSON File 로 분리하고 (D3-JSON), 없는 Key 를 확인한다 (D3-CHECK).
실행: 저장소 Root 에서  python3 app.py   (Windows: py -3 app.py)
"""

# 12 건의 합성 점검 기록. 실제 실험실 Data 가 아니다.
RECORDS = [
    {"date": "2026-08-03", "equipment_id": "HPLC-01", "status": "OK", "operator": "Kim"},
    {"date": "2026-08-04", "equipment_id": "HPLC-01", "status": "OK", "operator": "Lee"},
    {"date": "2026-08-05", "equipment_id": "GC-02", "status": "OK", "operator": "Kim"},
    {"date": "2026-08-06", "equipment_id": "HPLC-01", "status": "Warning", "operator": "Park"},
    {"date": "2026-08-07", "equipment_id": "HPLC-01", "status": "OK", "operator": "Kim"},
    {"date": "2026-08-10", "equipment_id": "CENT-03", "status": "OK", "operator": "Lee"},
    {"date": "2026-08-11", "equipment_id": "HPLC-01", "status": "OK", "operator": "Park"},
    {"date": "2026-08-12", "equipment_id": "HPLC-01", "status": "Warning", "operator": "Kim"},
    {"date": "2026-08-13", "equipment_id": "GC-02", "status": "OK", "operator": "Lee"},
    {"date": "2026-08-14", "equipment_id": "HPLC-01", "status": "OK", "operator": "Park"},
    {"date": "2026-08-17", "equipment_id": "CENT-03", "status": "OK", "operator": "Kim"},
    {"date": "2026-08-18", "equipment_id": "HPLC-01", "status": "OK", "operator": "Lee"},
]

# >>> TODO-GUIDED: D2-TARGET >>>
# Day 2: 검색할 장비를 바꿔 본다. 따옴표 안의 문자열만 바꾼다.
# 장비 ID 후보: "HPLC-01", "GC-02", "CENT-03"
# "ALL" 은 장비로 걸러내지 않고 12 건을 모두 보여 준다.
target_equipment = "ALL"
target_status = "ALL"
# <<< TODO-GUIDED: D2-TARGET <<<

# >>> TODO-GUIDED: D1-FMT >>>
# Day 1: 출력 모양을 바꿔 본다. 따옴표 안의 문자열만 바꾼다.
HEADER_TITLE = "장비 점검 기록"
HEADER_RULE = "----------------------------"
COLUMN_SEP = " | "
LABEL_DATE = "날짜"
LABEL_EQUIPMENT = "장비"
LABEL_STATUS = "상태"
# <<< TODO-GUIDED: D1-FMT <<<


def search(records, equipment_id, status):
    """조건에 맞는 기록만 남긴다. Day 3 에 records.py 의 find_records 로 옮긴다."""
    found = []
    # >>> TODO-GUIDED: D3-FILTER >>>
    # Day 3: 상태 조건을 추가해 검색을 좁힌다. if 한 덩어리를 더한다.
    for record in records:
        if equipment_id != "ALL" and record["equipment_id"] != equipment_id:
            continue
        found.append(record)
    # <<< TODO-GUIDED: D3-FILTER <<<
    return found


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
    found = search(RECORDS, target_equipment, target_status)
    printer = RecordPrinter()
    printer.print_all(found)


if __name__ == "__main__":
    main()
