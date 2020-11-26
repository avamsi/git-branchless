import contextlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterator, List, Optional, TextIO, cast

DUMMY_NAME = "Testy McTestface"
DUMMY_EMAIL = "test@example.com"
DUMMY_DATE = "Wed 29 Oct 12:34:56 2020 PDT"


def git(
    command: str,
    args: Optional[List[str]] = None,
    time: int = 0,
    check: bool = True,
) -> str:
    if args is None:
        args = []
    args = ["git", command, *args]

    # Required for determinism, as these values will be baked into the commit
    # hash.
    date = f"{DUMMY_DATE} -{time:02d}00"
    env = {
        "GIT_AUTHOR_NAME": DUMMY_NAME,
        "GIT_AUTHOR_EMAIL": DUMMY_EMAIL,
        "GIT_AUTHOR_DATE": date,
        "GIT_COMMITTER_NAME": DUMMY_NAME,
        "GIT_COMMITTER_EMAIL": DUMMY_EMAIL,
        "GIT_COMMITTER_DATE": date,
        # Fake "editor" which accepts the default contents of any commit
        # messages. Usually, we can set this with `git commit -m`, but we have
        # no such option for things such as `git rebase`, which may call `git
        # commit` later as a part of their execution.
        "GIT_EDITOR": "true",
    }
    env.update({k: v for k, v in os.environ.items() if k.startswith("COV_")})

    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        env=env,
        check=check,
    )
    return result.stdout.decode()


def git_commit_file(name: str, time: int, contents: Optional[str] = None) -> None:
    path = os.path.join(os.getcwd(), f"{name}.txt")
    with open(path, "w") as f:
        if contents is None:
            f.write(f"{name} contents\n")
        else:
            f.write(contents)
            f.write("\n")
    git("add", ["."])
    git("commit", ["-m", f"create {name}.txt"], time=time)


def git_resolve_file(name: str, contents: str) -> None:
    path = os.path.join(os.getcwd(), f"{name}.txt")
    with open(path, "w") as f:
        f.write(contents)
        f.write("\n")
    git("add", [path])


def git_init_repo() -> None:
    git("init")
    git_commit_file(name="initial", time=0)

    python_path = Path(__file__).parent.parent
    git(
        "config",
        [
            "alias.branchless",
            f"!env PYTHONPATH={python_path} {sys.executable} -m branchless",
        ],
    )

    # Silence some log-spam.
    git("config", ["advice.detachedHead", "false"])

    # Non-deterministic metadata (depends on current time).
    git("config", ["branchless.commitMetadata.relativeTime", "false"])

    git("branchless", ["init"])


def git_detach_head() -> None:
    git("checkout", ["--detach", "HEAD"])


def _rstrip_lines(lines: str) -> str:
    return "".join(line.rstrip() + "\n" for line in lines.splitlines())


def compare(actual: str, expected: str) -> None:
    actual = _rstrip_lines(actual)
    expected = _rstrip_lines(expected)
    print("Expected:")
    print(expected)
    if actual == expected:
        print("Actual (passed):")
    else:
        print("Actual (failed):")
    print(actual)
    assert actual == expected


class FileBasedCapture:
    """Wraps a `TextIO` by putting it in a temporary file.

    This is necessary for operations such as `subprocess.call`, which call
    `.fileno()` on the stream. This method is not available for in-memory
    `io.StringIO` instances.
    """

    def __init__(self, stream: TextIO) -> None:
        """Constructor.

        Args:
          stream: The handle to the underlying file to wrap.
        """
        self.stream = stream

    def getvalue(self) -> str:
        """Get the data that has been written to this stream so far.

        Must only be called once.
        """
        self.stream.seek(0)
        return self.stream.read()


@contextlib.contextmanager
def capture() -> Iterator[FileBasedCapture]:
    with tempfile.NamedTemporaryFile("r+") as f:
        yield FileBasedCapture(cast(TextIO, f))