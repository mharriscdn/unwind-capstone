# controller/timed_input.py
from __future__ import annotations

import sys
import time


def timed_input(prompt: str, timeout_seconds: int) -> str | None:
    """
    Cross-platform timed input.

    Returns:
      - a string (possibly empty) if user pressed Enter
      - None if timeout elapsed with no Enter pressed

    Notes:
      - Windows: uses msvcrt polling (works reliably on Windows 10/11).
      - Unix/macOS: uses select on sys.stdin.
    """
    # Windows path
    try:
        import msvcrt  # type: ignore

        sys.stdout.write(prompt)
        sys.stdout.flush()

        buf: list[str] = []
        start = time.time()

        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getwche()
                if ch in ("\r", "\n"):
                    sys.stdout.write("\n")
                    return "".join(buf).strip()
                if ch == "\b":
                    # Backspace (best effort)
                    if buf:
                        buf.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    buf.append(ch)

            if (time.time() - start) >= timeout_seconds:
                sys.stdout.write("\n")
                return None

            time.sleep(0.05)

    except ImportError:
        # Unix/macOS fallback
        import select

        sys.stdout.write(prompt)
        sys.stdout.flush()

        rlist, _, _ = select.select([sys.stdin], [], [], timeout_seconds)
        if rlist:
            line = sys.stdin.readline()
            return (line or "").strip()
        return None
