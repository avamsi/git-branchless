import io

import py
from branchless.__main__ import main

from helpers import compare, git_commit_file, git_init_repo


def test_help() -> None:
    with io.StringIO() as out:
        assert main(["--help"], out=out) == 0
        assert "usage: branchless" in out.getvalue()


def test_commands(tmpdir: py.path.local) -> None:
    with tmpdir.as_cwd():
        git_init_repo()
        git_commit_file(name="test", time=1)

        with io.StringIO() as out:
            main(["smartlog"], out=out)
            compare(
                actual=out.getvalue(),
                expected="""\
:
@ 3df4b935 (master) create test.txt
""",
            )

        with io.StringIO() as out:
            main(["hide", "3df4b935"], out=out)
            compare(
                actual=out.getvalue(),
                expected="""\
Hid commit: 3df4b935
To unhide this commit, run: git checkout 3df4b935
""",
            )
