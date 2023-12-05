import difflib
import filecmp
import os
import shutil
import sys
from pathlib import Path

import pytest

root = Path(__file__).parent
examples = list((root / "examples").iterdir())


def check_diffs(dcmp):
    print(f"check_diffs {dcmp.left} and {dcmp.right}")
    assert dcmp.left_only == []
    assert dcmp.right_only == []
    success = True
    for filename in dcmp.diff_files:
        success = False
        print(f"File with difference: {filename}")
        with (dcmp.left / filename).open() as fh:
            left_content = fh.readlines()
        with (dcmp.right / filename).open() as fh:
            right_content = fh.readlines()
        for row in difflib.unified_diff(left_content, right_content):
            print(row, end="")
        print()

    # assert dcmp.diff_files == []
    for sub_dcmp in dcmp.subdirs.values():
        success = check_diffs(sub_dcmp) and success
    return success


@pytest.mark.parametrize("example", examples)
def test_examples(example, tmpdir, request):
    print(example)
    os.environ["PYTHONPATH"] = str(root / "src")
    outdir = tmpdir / "out"
    cmd = f"{sys.executable} -m sssimp --input {root / 'examples' / example / 'input'} {outdir}"
    print(cmd)
    exit_code = os.system(cmd)
    assert exit_code == 0
    expected_output = root / "examples" / example / "output"
    save = request.config.getoption("--save")
    if save:
        if expected_output.exists():
            shutil.rmtree(expected_output)
        shutil.move(outdir, expected_output)
        return

    dcmp = filecmp.dircmp(expected_output, outdir)
    print(expected_output, outdir)
    assert check_diffs(dcmp), "Some files differ. See above using the -s flag of pytest"
