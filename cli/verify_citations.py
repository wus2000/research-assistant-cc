"""Verify BibTeX citations via researchclaw.literature.verify."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from researchclaw.literature.verify import verify_citations


def run_verify(bib_text_or_path: str) -> str:
    """Run citation verification. Input can be BibTeX text or a file path."""
    path = Path(bib_text_or_path)
    if path.is_file():
        bib_text = path.read_text(encoding="utf-8")
    else:
        bib_text = bib_text_or_path
    report = verify_citations(bib_text=bib_text)
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False, default=str)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Verify BibTeX citations")
    parser.add_argument(
        "--bib",
        required=True,
        help="BibTeX text or path to .bib file",
    )
    args = parser.parse_args()
    try:
        print(run_verify(args.bib))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
