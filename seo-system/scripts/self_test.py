#!/usr/bin/env python3
"""Run the OneTap SEO system against the bundled sample site."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, check=True)


def main() -> None:
    system = Path(__file__).resolve().parents[1]
    sample = system / "examples" / "sample-site"
    output = sample / "seo-output"
    run([sys.executable, str(system / "scripts" / "build_seo.py"), "--config", str(sample / "client-seo.config.json"), "--output", str(output), "--production"])
    run([sys.executable, str(system / "scripts" / "audit_seo.py"), "--config", str(sample / "client-seo.config.json"), "--site-dir", str(sample), "--production", "--report", str(output / "prelaunch-audit.md")])
    print("OneTap SEO system self-test passed.")


if __name__ == "__main__":
    main()
