"""Midnight Fridge Roast (make.fun judged-artifact entry) — root entrypoint.

The whole entry is one line of text. This program writes it to /output/entry.txt and
nothing else:

  * exact bytes of one line, UTF-8, no trailing newline, ASCII only;
  * mode 0644 on the artifact itself (the sandbox's watcher reads the program's
    mode-644 file and is refused a mode-600 file, so the temp file is chmod'ed
    BEFORE it takes the artifact's name);
  * atomic: written to a temp file in the same directory, fsynced, then os.replace;
  * the gate's caps (UTF-8 text of 1..200 characters, not only white space, one line)
    are re-checked here, with a short safe fallback line, so this entry can never be
    gated out by an edit to the text above;
  * stdout reports what was actually left on disk: bytes, characters, mode, sha256.
"""

import hashlib
import os
import stat
import tempfile

OUTDIR_ENV = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTDIR = "/output"
ARTIFACT = "entry.txt"

MIN_CHARS = 1
MAX_CHARS = 200

ENTRY = (
    "My fridge won't open after midnight. 'You'll thank me in the morning,' it says, "
    "which is bold from a box holding four kinds of cheese hostage."
)

# Used only if ENTRY ever failed the gate's caps: still a valid one-line roast of the
# fridge's midnight refusal, so the artifact is never blank or oversized.
FALLBACK = "My fridge won't open after midnight, and honestly, that feels like a decision it made about me."


def out_dir() -> str:
    """The graded output directory: the sandbox's mount, else the rules' path."""
    return os.environ.get(OUTDIR_ENV) or DEFAULT_OUTDIR


def gate_problems(text: str) -> list[str]:
    """Everything about `text` the gate would refuse, in the gate's own terms."""
    problems: list[str] = []
    if "\n" in text or "\r" in text:
        problems.append("not one line (a newline is present)")
    if text != text.strip():
        problems.append("leading or trailing white space")
    if not text.strip():
        problems.append("only white space")
    n = len(text)
    if n < MIN_CHARS or n > MAX_CHARS:
        problems.append(f"{n} characters, outside {MIN_CHARS}..{MAX_CHARS}")
    if any(ord(c) < 32 or ord(c) == 127 for c in text):
        problems.append("holds a control character")
    return problems


def choose_text() -> tuple[str, list[str]]:
    """The entry, or the fallback when the entry would fail the gate."""
    problems = gate_problems(ENTRY)
    if not problems:
        return ENTRY, []
    return FALLBACK, problems


def write_atomic(path: str, data: bytes) -> None:
    """Put exactly `data` at `path`, atomically, with mode 0644 on the artifact."""
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        # mkstemp creates 0600: set 0644 before the file takes the artifact's name,
        # so the graded path is never a mode-600 one.
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main() -> int:
    text, problems = choose_text()
    if problems:
        print("entry text failed the gate's caps, using the fallback: " + "; ".join(problems))

    data = text.encode("utf-8")
    out = out_dir()
    path = os.path.join(out, ARTIFACT)
    write_atomic(path, data)

    # The file the grader reads, read back: its own bytes and its own mode.
    on_disk = open(path, "rb").read()
    if os.stat(path).st_mode & 0o777 != 0o644:
        os.chmod(path, 0o644)
    mode = stat.S_IMODE(os.stat(path).st_mode)

    print(
        "entry.txt: "
        f"{len(on_disk)} bytes, {len(on_disk.decode('utf-8'))} characters, "
        f"mode {mode:04o}, sha256 {hashlib.sha256(on_disk).hexdigest()}"
    )
    print("text: " + on_disk.decode("utf-8"))

    if on_disk != data or mode != 0o644:
        print("ERROR: the artifact on disk does not match what was written")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
