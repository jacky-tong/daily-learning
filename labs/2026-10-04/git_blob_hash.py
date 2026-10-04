#!/usr/bin/env python3
"""Compute a traditional Git blob SHA-1 without calling Git."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def git_blob_sha1(content: bytes) -> str:
    """Return the SHA-1 object id Git assigns to blob content."""
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def run_self_test() -> None:
    # This is the documented Git blob id for the bytes b"test content\n".
    expected = "d670460b4b4aece5915caf5c68d12f560a9fe3e4"
    actual = git_blob_sha1(b"test content\n")
    assert actual == expected, f"expected {expected}, got {actual}"
    print("self-test passed")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute the SHA-1 of a Git blob object."
    )
    parser.add_argument("path", nargs="?", type=Path, help="file to hash")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return
    if args.path is None:
        parser.error("provide a file path or use --self-test")
    print(git_blob_sha1(args.path.read_bytes()))


if __name__ == "__main__":
    main()

