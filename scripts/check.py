"""check.py — 실습 Block 이 의도대로 끝났는지 확인한다.

사용: 저장소 Root 에서
    python3 scripts/check.py <BLOCK-ID>    (Windows: py -3 scripts/check.py <BLOCK-ID>)
    python3 scripts/check.py ENV           설치 상태 확인

출력은 항상 [PASS] 또는 [FAIL] 로 시작하고, 통과하면 [NEXT] 로 다음 Block 을 알려 준다.
Day 1 의 검사는 출력 모양을 보지 않는다. Data 가 그대로인지, Block 을 정말 바꿨는지만 본다.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKPOINTS = ROOT / "checkpoints"
ORDER = ["D1-FMT", "D2-TARGET", "D3-FILTER", "D3-EXTRACT", "D3-JSON", "D3-CHECK", "D4-IMPORT"]
BLOCK_FILE = {
    "D1-FMT": "app.py",
    "D2-TARGET": "app.py",
    "D3-FILTER": "app.py",
    "D3-EXTRACT": "records.py",
    "D3-JSON": "app.py",
    "D3-CHECK": "records.py",
    "D4-IMPORT": "notebooks/analysis.ipynb",
}
MIN_LINES, MAX_LINES = 5, 15
OPEN = re.compile(r"^\s*# >>> TODO-GUIDED: ([A-Z0-9-]+) >>>\s*$")
CLOSE = re.compile(r"^\s*# <<< TODO-GUIDED: ([A-Z0-9-]+) <<<\s*$")


def ok(block_id, message=""):
    print(f"[PASS] {block_id}" + (f": {message}" if message else ""))
    if block_id in ORDER and ORDER.index(block_id) + 1 < len(ORDER):
        print(f"[NEXT] {ORDER[ORDER.index(block_id) + 1]}")
    elif block_id in ORDER:
        print("[NEXT] Day 4 마무리: Branch 를 Push 하고 개인 Pull Request 를 만드세요.")
    return 0


def fail(block_id, message):
    print(f"[FAIL] {block_id}: {message}")
    return 1


def block_lines(text, block_id):
    """마커 사이의 줄들을 돌려준다. 마커가 없거나 짝이 맞지 않으면 None."""
    lines = text.splitlines()
    start = end = None
    for i, line in enumerate(lines):
        m = OPEN.match(line)
        if m and m.group(1) == block_id:
            start = i
        m = CLOSE.match(line)
        if m and m.group(1) == block_id and start is not None:
            end = i
            break
    if start is None or end is None:
        return None
    return lines[start + 1:end]


def notebook_code(path):
    nb = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")


def load_block(block_id):
    target = ROOT / BLOCK_FILE[block_id]
    if not target.is_file():
        return None, f"{BLOCK_FILE[block_id]} 가 없습니다."
    text = notebook_code(target) if target.suffix == ".ipynb" else target.read_text(encoding="utf-8")
    lines = block_lines(text, block_id)
    if lines is None:
        return None, f"{BLOCK_FILE[block_id]} 에서 {block_id} 마커 쌍을 찾지 못했습니다."
    if not MIN_LINES <= len(lines) <= MAX_LINES:
        return None, f"마커 사이 줄 수가 {len(lines)} 입니다 ({MIN_LINES}~{MAX_LINES} 줄이어야 합니다)."
    return lines, None


def run_app():
    result = subprocess.run([sys.executable, "app.py"], cwd=ROOT, capture_output=True, text=True)
    return result.returncode, result.stdout.splitlines(), result.stderr.strip()


def data_invariants(records):
    """12 건, HPLC-01 8 건, Warning 2 건."""
    return (
        len(records) == 12
        and sum(r.get("equipment_id") == "HPLC-01" for r in records) == 8
        and sum(r.get("status") == "Warning" for r in records) == 2
    )


def check_d1():
    lines, err = load_block("D1-FMT")
    if err:
        return fail("D1-FMT", err)
    baseline = block_lines((CHECKPOINTS / "D1-FMT" / "app.py").read_text(encoding="utf-8"), "D1-FMT")
    if lines == baseline:
        return fail("D1-FMT", "Block 이 아직 시작 상태와 같습니다. 따옴표 안 문자열을 하나 이상 바꾸세요.")
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and re.search(r"\b(record|RECORDS|records)\s*\[", stripped):
            return fail("D1-FMT", "Day 1 Block 에는 따옴표 안 문자열만 바꿉니다. 대괄호로 기록을 꺼내는 것은 Day 3 에 배웁니다.")
    code, out, err_text = run_app()
    if code != 0:
        return fail("D1-FMT", f"app.py 가 실패했습니다.\n{err_text}")
    if len(out) != 14:
        return fail("D1-FMT", f"출력이 {len(out)} 줄입니다. 머리 2 줄 + 기록 12 줄 = 14 줄이어야 합니다.")
    body = out[2:]
    if sum("HPLC-01" in line for line in body) != 8 or sum("Warning" in line for line in body) != 2:
        return fail("D1-FMT", "기록 12 줄 안에 HPLC-01 8 건, Warning 2 건이 보여야 합니다.")
    return ok("D1-FMT", "출력 모양이 바뀌었고 기록 12 건은 그대로입니다.")


def check_d2():
    lines, err = load_block("D2-TARGET")
    if err:
        return fail("D2-TARGET", err)
    code, out, err_text = run_app()
    if code != 0:
        return fail("D2-TARGET", f"app.py 가 실패했습니다.\n{err_text}")
    if len(out) < 3:
        return fail("D2-TARGET", "검색 결과가 0 건입니다. 장비 ID 의 철자를 확인하세요 (HPLC-01, GC-02, CENT-03).")
    if len(out) == 14:
        return fail("D2-TARGET", "아직 12 건이 모두 나옵니다. target_equipment 를 하나의 장비로 바꾸세요.")
    return ok("D2-TARGET", f"{len(out) - 2} 건으로 좁혀졌습니다.")


def check_d3_filter():
    lines, err = load_block("D3-FILTER")
    if err:
        return fail("D3-FILTER", err)
    if not any("status" in line for line in lines if not line.strip().startswith("#")):
        return fail("D3-FILTER", "Block 안에 status 조건이 보이지 않습니다.")
    code, out, err_text = run_app()
    if code != 0:
        return fail("D3-FILTER", f"app.py 가 실패했습니다.\n{err_text}")
    if len(out) - 2 != 2:
        return fail("D3-FILTER", f"Warning 만 남기면 2 건이어야 하는데 {len(out) - 2} 건입니다.")
    return ok("D3-FILTER", "Warning 2 건만 남았습니다.")


def import_find_records():
    sys.path.insert(0, str(ROOT))
    for name in ("records",):
        sys.modules.pop(name, None)
    import records  # noqa: E402

    return records.find_records


def check_d3_extract():
    if not (ROOT / "records.py").is_file():
        return fail("D3-EXTRACT", "records.py 가 없습니다. 검색 Function 을 새 File 로 옮기세요.")
    lines, err = load_block("D3-EXTRACT")
    if err:
        return fail("D3-EXTRACT", err)
    app_text = (ROOT / "app.py").read_text(encoding="utf-8")
    if "class RecordPrinter" not in app_text:
        return fail("D3-EXTRACT", "RecordPrinter 는 app.py 에 남아 있어야 합니다.")
    if "from records import find_records" not in app_text:
        return fail("D3-EXTRACT", "app.py 가 records.py 의 find_records 를 import 해야 합니다.")
    if "def search(" in app_text:
        return fail("D3-EXTRACT", "옮긴 뒤 app.py 의 옛 search 는 지웁니다. 같은 Logic 을 두 곳에 두지 않습니다.")
    try:
        find_records = import_find_records()
    except Exception as exc:  # noqa: BLE001 — Traceback 을 그대로 보여 준다
        return fail("D3-EXTRACT", f"records.py 를 import 하지 못했습니다.\n{type(exc).__name__}: {exc}")
    sample = json.loads((CHECKPOINTS / "D3-JSON" / "experiment_records.json").read_text(encoding="utf-8"))
    if len(find_records(sample, "HPLC-01", "ALL")) != 8 or len(find_records(sample, "ALL", "Warning")) != 2:
        return fail("D3-EXTRACT", "find_records(records, equipment_id, status) 가 8 건 / 2 건을 돌려주지 않습니다.")
    if find_records(sample, "NOPE-99", "ALL") != []:
        return fail("D3-EXTRACT", "없는 장비를 찾으면 빈 List 가 나와야 합니다.")
    code, out, err_text = run_app()
    if code != 0:
        return fail("D3-EXTRACT", f"app.py 가 실패했습니다.\n{err_text}")
    return ok("D3-EXTRACT", "검색은 records.py 로, 출력은 app.py 에 남았습니다.")


def check_d3_json():
    lines, err = load_block("D3-JSON")
    if err:
        return fail("D3-JSON", err)
    if not (ROOT / "experiment_records.json").is_file():
        return fail("D3-JSON", "experiment_records.json 이 저장소 Root 에 없습니다.")
    app_text = (ROOT / "app.py").read_text(encoding="utf-8")
    if "json.load" not in app_text:
        return fail("D3-JSON", "app.py 가 json.load 로 File 을 읽어야 합니다.")
    if re.search(r'RECORDS = \[\s*\{', app_text):
        return fail("D3-JSON", "Code 안에 박힌 RECORDS List 가 아직 남아 있습니다.")
    records = json.loads((ROOT / "experiment_records.json").read_text(encoding="utf-8"))
    if not data_invariants(records):
        return fail("D3-JSON", "JSON 의 기록이 12 건 / HPLC-01 8 건 / Warning 2 건이 아닙니다.")
    code, out, err_text = run_app()
    if code != 0:
        return fail("D3-JSON", f"app.py 가 실패했습니다 (저장소 Root 에서 실행했나요?).\n{err_text}")
    return ok("D3-JSON", "기록이 Code 밖 JSON File 에서 들어옵니다.")


def check_d3_check():
    lines, err = load_block("D3-CHECK")
    if err:
        return fail("D3-CHECK", err)
    try:
        find_records = import_find_records()
    except Exception as exc:  # noqa: BLE001
        return fail("D3-CHECK", f"records.py 를 import 하지 못했습니다.\n{type(exc).__name__}: {exc}")
    broken = [{"date": "2026-08-03", "equipment_id": "HPLC-01"}]
    try:
        find_records(broken, "ALL", "ALL")
    except KeyError as exc:
        if "status" not in str(exc):
            return fail("D3-CHECK", "없는 Key 의 이름('status')이 오류 Message 에 보여야 합니다.")
    except Exception as exc:  # noqa: BLE001
        return fail("D3-CHECK", f"KeyError 가 아닌 {type(exc).__name__} 가 났습니다.")
    else:
        return fail("D3-CHECK", "status 가 없는 기록을 넣었는데 오류가 나지 않았습니다. 명시적 확인을 추가하세요.")
    good = json.loads((ROOT / "experiment_records.json").read_text(encoding="utf-8"))
    if len(find_records(good, "ALL", "Warning")) != 2:
        return fail("D3-CHECK", "정상 기록에서는 여전히 Warning 2 건이 나와야 합니다.")
    return ok("D3-CHECK", "깨진 기록은 무엇이 없는지 말하고, 정상 기록은 그대로 처리합니다.")


def check_d4():
    lines, err = load_block("D4-IMPORT")
    if err:
        return fail("D4-IMPORT", err)
    joined = "\n".join(lines)
    if "from records import find_records" not in joined:
        return fail("D4-IMPORT", "Notebook 이 records.py 의 find_records 를 import 해야 합니다.")
    nb_code = notebook_code(ROOT / "notebooks" / "analysis.ipynb")
    if "for record in" in nb_code and "found.append" in nb_code:
        return fail("D4-IMPORT", "복사된 검색 Loop 가 아직 Notebook 에 남아 있습니다. import 한 Function 호출로 바꾸세요.")
    try:
        find_records = import_find_records()
    except Exception as exc:  # noqa: BLE001
        return fail("D4-IMPORT", f"records.py 를 import 하지 못했습니다.\n{type(exc).__name__}: {exc}")
    good = json.loads((ROOT / "experiment_records.json").read_text(encoding="utf-8"))
    cli_counts = {e: len(find_records(good, e, "Warning")) for e in ("HPLC-01", "GC-02", "CENT-03")}
    # Notebook 의 Code Cell 을 위에서 아래로 실제로 실행한다 (Restart and Run All 과 같은 순서, 새 namespace).
    nb_source = notebook_code(ROOT / "notebooks" / "analysis.ipynb").replace("counts  #", "counts_result = counts  #")
    namespace = {"__name__": "__notebook__"}
    try:
        exec(compile(nb_source, "notebooks/analysis.ipynb", "exec"), namespace)  # noqa: S102 — 학생 Notebook 을 그대로 실행
    except Exception as exc:  # noqa: BLE001 — Traceback 을 그대로 보여 준다
        return fail("D4-IMPORT", f"Notebook 을 처음부터 실행하면 실패합니다 (Restart and Run All 과 같은 결과).\n{type(exc).__name__}: {exc}")
    nb_counts = namespace.get("counts")
    if nb_counts != cli_counts or list(cli_counts.values()) != [2, 0, 0]:
        return fail("D4-IMPORT", f"CLI 는 {cli_counts}, Notebook 은 {nb_counts} 입니다. 장비별 Warning 건수는 2/0/0 으로 같아야 합니다.")
    return ok("D4-IMPORT", "CLI 와 Notebook 이 같은 Module 로 같은 숫자 2/0/0 을 냅니다.")


def check_env():
    print(f"interpreter : {sys.executable}")
    print(f"python      : {sys.version.split()[0]}")
    git = shutil.which("git")
    git_version = ""
    if git:
        git_version = subprocess.run([git, "--version"], capture_output=True, text=True).stdout.strip()
    print(f"git         : {git_version or '(없음)'}")
    problems = []
    if sys.version_info < (3, 11):
        problems.append("Python 3.11 이상이 필요합니다.")
    if not git:
        problems.append("git 이 PATH 에 없습니다.")
    else:
        m = re.search(r"(\d+)\.(\d+)", git_version)
        if m and (int(m.group(1)), int(m.group(2))) < (2, 23):
            problems.append("git 2.23 이상이 필요합니다 (git restore).")
    if problems:
        return fail("ENV", " / ".join(problems))
    print("[PASS] ENV: 이 명령이 동작한 Interpreter 를 수업 내내 그대로 쓰세요.")
    return 0


CHECKS = {
    "D1-FMT": check_d1,
    "D2-TARGET": check_d2,
    "D3-FILTER": check_d3_filter,
    "D3-EXTRACT": check_d3_extract,
    "D3-JSON": check_d3_json,
    "D3-CHECK": check_d3_check,
    "D4-IMPORT": check_d4,
    "ENV": check_env,
}


def main(argv):
    if len(argv) != 2:
        return fail("check", f"BLOCK-ID 하나가 필요합니다. 가능한 값: {', '.join(CHECKS)}")
    block_id = argv[1].strip().upper()
    if block_id not in CHECKS:
        return fail(block_id, f"알 수 없는 BLOCK-ID. 가능한 값: {', '.join(CHECKS)}")
    return CHECKS[block_id]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
