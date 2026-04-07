"""Check research novelty via researchclaw.literature.novelty."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from researchclaw.literature.novelty import check_novelty


def run_novelty(topic: str, hypotheses_or_path: str) -> str:
    """Run novelty check. hypotheses_or_path can be text or a file path."""
    path = Path(hypotheses_or_path)
    if path.is_file():
        hypotheses_text = path.read_text(encoding="utf-8")
    else:
        hypotheses_text = hypotheses_or_path

    result = check_novelty(topic=topic, hypotheses_text=hypotheses_text)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Check research novelty")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument(
        "--hypotheses",
        required=True,
        help="Hypotheses text or path to .md file",
    )
    args = parser.parse_args()
    try:
        print(run_novelty(args.topic, args.hypotheses))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
