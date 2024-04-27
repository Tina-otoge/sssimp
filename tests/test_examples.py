import difflib
import filecmp
import os
import shutil
import sys
from pathlib import Path

import pytest

root = Path(".")
examples = root.glob("examples/*/")


def check_diffs(diff, example):
    assert diff.left_only == []
    assert diff.right_only == []
    success = True
    for filename in diff.diff_files:
        success = False
        print(f"File with difference: {example / filename}")
        left_content = (
            (Path(diff.left) / filename).read_text().splitlines(keepends=True)
        )
        right_content = (
            (Path(diff.right) / filename).read_text().splitlines(keepends=True)
        )
        for row in difflib.unified_diff(left_content, right_content):
            print(row, end="")
        print()

    for sub_dcmp in diff.subdirs.values():
        success = check_diffs(sub_dcmp, example) and success
    return success


@pytest.mark.parametrize("example", examples)
def test_examples(example, tmpdir, request):
    outdir = tmpdir / "output"
    cmd = f"sssimp --input {example / 'input'} {outdir}"
    print(cmd)
    exit_code = os.system(cmd)
    assert exit_code == 0
    expected_output = root / example / "output"
    save = request.config.getoption("--save")
    if save:
        if expected_output.exists():
            shutil.rmtree(expected_output)
        shutil.move(outdir, expected_output)
        return

    diff = filecmp.dircmp(expected_output, outdir)
    print(expected_output, outdir)
    assert check_diffs(
        diff,
        example,
    ), "Some files differ. See above using the -s flag of pytest"
