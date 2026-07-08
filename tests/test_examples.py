import difflib
import filecmp
import os
import shutil
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageChops

root = Path(".")
examples = sorted(root.glob("examples/*/"))


def images_equal(left_path, right_path):
    try:
        with Image.open(left_path) as left, Image.open(right_path) as right:
            if left.size != right.size or left.mode != right.mode:
                return False
            return ImageChops.difference(left, right).getbbox() is None
    except OSError:
        return False


def check_diffs(diff, example):
    assert diff.left_only == []
    assert diff.right_only == []
    success = True
    for filename in diff.diff_files:
        print(f"File with difference: {example / filename}")
        left_path = Path(diff.left) / filename
        right_path = Path(diff.right) / filename
        try:
            left_content = left_path.read_text().splitlines(keepends=True)
            right_content = right_path.read_text().splitlines(keepends=True)
        except UnicodeDecodeError:
            if images_equal(left_path, right_path):
                continue
            if left_path.read_bytes() != right_path.read_bytes():
                success = False
                print("Binary files differ")
            continue
        success = False
        for row in difflib.unified_diff(left_content, right_content):
            print(row, end="")
        print()

    for sub_dcmp in diff.subdirs.values():
        success = check_diffs(sub_dcmp, example) and success
    return success


@pytest.mark.parametrize("example", examples, ids=lambda e: e.name)
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
