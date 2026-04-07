#!/usr/bin/env python3
"""Unified CLI entry point for research-assistant tools.

Usage:
    python research_cli.py search "query" [--limit N] [--year-min YYYY] [--sources s1,s2]
    python research_cli.py novelty --topic "..." --hypotheses "text or path"
    python research_cli.py verify --bib "bibtex text or path"
    python research_cli.py domain --topic "..."
"""
from __future__ import annotations

import sys


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: research_cli.py <command> [args]\n"
            "Commands: search, novelty, verify, domain",
            file=sys.stderr,
        )
        sys.exit(1)

    command = sys.argv[1]
    sys.argv = [sys.argv[0]] + sys.argv[2:]

    if command == "search":
        from search_papers import main as search_main
        search_main()
    elif command == "novelty":
        from check_novelty import main as novelty_main
        novelty_main()
    elif command == "verify":
        from verify_citations import main as verify_main
        verify_main()
    elif command == "domain":
        from detect_domain import main as domain_main
        domain_main()
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available: search, novelty, verify, domain", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
