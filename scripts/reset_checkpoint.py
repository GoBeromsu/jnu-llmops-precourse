"""reset_checkpoint.py — 예정된 실패에서 알려진 정상 상태로 되돌린다.

사용: 저장소 Root 에서
    python3 scripts/reset_checkpoint.py <BLOCK-ID>      (Windows: py -3 scripts/reset_checkpoint.py <BLOCK-ID>)

BLOCK-ID 별 동작:
    D1-FMT      app.py 를 마지막 Commit 상태로 되돌린다 (Stage 여부와 상관없이). 여러분의 Commit 은 남는다.
    D2-TARGET   checkpoints/D2-TARGET/ 의 정본을 app.py 위에 덮어쓴다. Commit 하지 않은 상태로 둔다.
    D3-FILTER   checkpoints/D3-FILTER/  → app.py
    D3-EXTRACT  checkpoints/D3-EXTRACT/ → app.py, records.py
    D3-JSON     checkpoints/D3-JSON/    → app.py, records.py, experiment_records.json
    D3-CHECK    checkpoints/D3-CHECK/   → app.py, records.py, experiment_records.json
    DAY4-START  Day 3 완성 상태로 전원을 맞춘다 (= D3-CHECK 정본).
    D4-IMPORT   checkpoints/D4-IMPORT/analysis.ipynb → notebooks/analysis.ipynb

덮어쓴 File 은 Stage 하지 않는다. git diff 로 무엇이 바뀌었는지 먼저 읽고 Commit 한다.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKPOINTS = ROOT / "checkpoints"

# BLOCK-ID -> (checkpoint 디렉터리 이름, [(정본 상대 경로, 대상 상대 경로), ...])
TARGETS = {
    "D2-TARGET": ("D2-TARGET", [("app.py", "app.py")]),
    "D3-FILTER": ("D3-FILTER", [("app.py", "app.py")]),
    "D3-EXTRACT": ("D3-EXTRACT", [("app.py", "app.py"), ("records.py", "records.py")]),
    "D3-JSON": ("D3-JSON", [("app.py", "app.py"), ("records.py", "records.py"),
                            ("experiment_records.json", "experiment_records.json")]),
    "D3-CHECK": ("D3-CHECK", [("app.py", "app.py"), ("records.py", "records.py"),
                              ("experiment_records.json", "experiment_records.json")]),
    "DAY4-START": ("DAY4-START", [("app.py", "app.py"), ("records.py", "records.py"),
                                  ("experiment_records.json", "experiment_records.json")]),
    "D4-IMPORT": ("D4-IMPORT", [("analysis.ipynb", "notebooks/analysis.ipynb")]),
}
VALID = ["D1-FMT", *TARGETS]


def fail(message):
    print(f"[FAIL] {message}")
    return 1


def restore_day1():
    result = subprocess.run(
        ["git", "restore", "--source=HEAD", "--staged", "--worktree", "--", "app.py"],
        cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        return fail(f"D1-FMT: git restore 실패 — {result.stderr.strip()}")
    print("[PASS] D1-FMT: app.py 의 Commit 되지 않은 변경을 버렸습니다. 여러분의 Commit 은 그대로 있습니다.")
    print("[NEXT] python3 app.py 로 다시 실행하고, git diff 가 비어 있는지 확인하세요.")
    return 0


def restore_from_checkpoint(block_id):
    folder, pairs = TARGETS[block_id]
    source_dir = CHECKPOINTS / folder
    if not source_dir.is_dir():
        return fail(f"{block_id}: 정본 폴더가 없습니다 — {source_dir}")
    missing = [source_dir / src_name for src_name, _ in pairs if not (source_dir / src_name).is_file()]
    if missing:
        return fail(f"{block_id}: 정본 File 이 없습니다 — {', '.join(str(m) for m in missing)} (아무 File 도 바꾸지 않았습니다)")
    for src_name, dst_name in pairs:
        src = source_dir / src_name
        dst = ROOT / dst_name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        print(f"[PASS] {block_id}: {dst_name} 를 정본으로 덮어썼습니다 (Stage 하지 않음).")
    print("[NEXT] git diff 로 무엇이 달라졌는지 읽은 뒤 python3 app.py 로 다시 실행하세요.")
    return 0


def main(argv):
    if len(argv) != 2:
        return fail(f"BLOCK-ID 하나가 필요합니다. 가능한 값: {', '.join(VALID)}")
    block_id = argv[1].strip().upper()
    if block_id == "D1-FMT":
        return restore_day1()
    if block_id in TARGETS:
        return restore_from_checkpoint(block_id)
    return fail(f"알 수 없는 BLOCK-ID '{argv[1]}'. 가능한 값: {', '.join(VALID)}")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
