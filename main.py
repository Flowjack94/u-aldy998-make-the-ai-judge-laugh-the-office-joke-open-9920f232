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
    """Reject anything that is not one clean line of 1-200 characters.

    Also rejects C1 controls (U+0080-U+009F), the U+FFFD replacement
    character (a sign of undecodable input), and lone surrogates
    (U+D800-U+DFFF), which cannot round-trip through UTF-8.
    """
    if not text or not text.strip():
        raise ValueError("entry is empty or whitespace-only")
    if len(text) > 200:
        raise ValueError(f"entry is {len(text)} characters, over the 200 limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry contains a line break")
    for ch in text:
        code = ord(ch)
        if code < 0x20 or code == 0x7F or 0x80 <= code <= 0x9F:
            raise ValueError(f"entry contains a control character U+{code:04X}")
        if code == 0xFFFD:
            raise ValueError("entry contains a replacement character U+FFFD")
        if 0xD800 <= code <= 0xDFFF:
            raise ValueError(f"entry contains a lone surrogate U+{code:04X}")


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
