#!/usr/bin/env python3
"""Make the AI Judge Laugh: the Office Joke Open.

Writes exactly one line — an original joke about office life — to
/output/entry.txt. The joke is validated before it is written: it must be
a single line of 1-200 UTF-8 characters, with no control characters, no
line breaks, and no leading or trailing whitespace.
"""

import hashlib
import os

ENTRY = "We had a meeting to decide whether we need a meeting. The meeting decided: yes, weekly, forever."

OUTPUT_PATH = "/output/entry.txt"


def validate_entry(text: str) -> None:
    """Reject anything that is not one clean line of 1-200 characters."""
    if not text or not text.strip():
        raise ValueError("entry is empty or whitespace-only")
    if len(text) > 200:
        raise ValueError(f"entry is {len(text)} characters, over the 200 limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry contains a line break")
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError(f"entry contains a control character U+{ord(ch):04X}")


def main() -> None:
    validate_entry(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(OUTPUT_PATH, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(ENTRY)
    print(f"chars: {len(ENTRY)}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
