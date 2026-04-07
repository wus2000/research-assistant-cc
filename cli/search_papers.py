"""Search academic papers via researchclaw.literature.

Wraps search_papers() to return JSON to stdout.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Sequence

from researchclaw.literature.search import search_papers


def format_paper_json(paper: Any) -> dict[str, Any]:
    """Convert a Paper object to a JSON-serializable dict."""
    authors = [a.name for a in paper.authors] if paper.authors else []
    return {
        "title": paper.title,
        "authors": authors,
        "year": paper.year,
        "venue": paper.venue,
        "citation_count": paper.citation_count,
        "doi": paper.doi,
        "arxiv_id": paper.arxiv_id,
        "url": paper.url,
        "abstract": paper.abstract,
        "cite_key": paper.cite_key,
    }


def run_search(
    query: str,
    *,
    limit: int = 10,
    year_min: int = 0,
    sources: Sequence[str] = ("openalex", "semantic_scholar", "arxiv"),
) -> str:
    """Execute search and return JSON string."""
    papers = search_papers(
        query, limit=limit, year_min=year_min, sources=sources, deduplicate=True,
    )
    results = [format_paper_json(p) for p in papers]
    return json.dumps(results, indent=2, ensure_ascii=False)


def main() -> None:
    """CLI entry point. Called by research_cli.py."""
    import argparse

    parser = argparse.ArgumentParser(description="Search academic papers")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Max results per source")
    parser.add_argument("--year-min", type=int, default=0, help="Minimum publication year")
    parser.add_argument("--sources", default="openalex,semantic_scholar,arxiv",
                        help="Comma-separated sources")
    args = parser.parse_args()

    sources = tuple(s.strip() for s in args.sources.split(","))
    try:
        print(run_search(args.query, limit=args.limit, year_min=args.year_min, sources=sources))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
