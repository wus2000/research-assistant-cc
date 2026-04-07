#!/usr/bin/env python3
"""Research Assistant MCP Server.

Exposes academic search, novelty checking, citation verification,
domain detection, and session management as MCP tools.

All research tools accept an optional session_id parameter for
concurrent-safe context isolation. Without session_id, tools
operate statelessly (no context read/write).

Usage:
    python server.py              # stdio transport (default for Claude Code)
    python server.py --transport sse --port 8765  # SSE for debugging
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

# Add cli directory to path for imports
_CLI_DIR = Path(__file__).parent.parent / "cli"
sys.path.insert(0, str(_CLI_DIR))

from search_papers import run_search, format_paper_json
from check_novelty import run_novelty
from verify_citations import run_verify
from detect_domain import run_detect, format_profile_json
from session_manager import (
    new_session,
    list_sessions,
    switch_session,
    get_current_session,
    get_context_path,
    migrate_legacy_context,
)

mcp = FastMCP(
    "research-assistant",
    instructions=(
        "AI research assistant with academic search, novelty assessment, "
        "citation verification, domain detection, and session management. "
        "Use research_session_new() first to create an isolated session, "
        "then pass the returned session_id to all subsequent tool calls."
    ),
)


# ---------------------------------------------------------------------------
# Session management tools
# ---------------------------------------------------------------------------


@mcp.tool()
def research_session_new(topic: str) -> str:
    """Create a new isolated research session for a topic.

    Returns a globally unique session_id (date-slug-uuid8).
    IMPORTANT: Save the returned session_id and pass it to all
    subsequent research tool calls for concurrent-safe isolation.

    Args:
        topic: Research topic name (e.g. "vision transformer pruning")
    """
    result = new_session(topic)
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
def research_session_list() -> str:
    """List all research sessions with their status and files."""
    result = list_sessions()
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
def research_session_switch(session_id: str) -> str:
    """Switch the convenience symlink to an existing session.

    Args:
        session_id: Session ID from research_session_list
    """
    result = switch_session(session_id)
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
def research_session_current() -> str:
    """Show the session currently pointed to by the convenience symlink."""
    result = get_current_session()
    return json.dumps(result, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Research tools (all accept optional session_id for concurrency safety)
# ---------------------------------------------------------------------------


@mcp.tool()
def search_papers(
    query: str,
    limit: int = 5,
    year_min: int = 0,
    sources: str = "openalex,semantic_scholar,arxiv",
    session_id: str = "",
) -> str:
    """Search academic papers across OpenAlex, Semantic Scholar, and arXiv.

    Returns deduplicated results sorted by citation count.
    If session_id is provided, results are also saved to that session's context.

    Args:
        query: Search query (e.g. "vision transformer pruning")
        limit: Maximum results per source (default 10)
        year_min: Minimum publication year (0 = no filter)
        sources: Comma-separated sources: openalex, semantic_scholar, arxiv
        session_id: Session ID for context isolation (from research_session_new)
    """
    source_tuple = tuple(s.strip() for s in sources.split(","))
    result_json = run_search(query, limit=limit, year_min=year_min, sources=source_tuple)

    # Persist to session context if session_id provided
    if session_id:
        ctx = get_context_path(session_id)
        lit_file = ctx / "literature.jsonl"
        papers = json.loads(result_json)
        with lit_file.open("a", encoding="utf-8") as f:
            for paper in papers:
                f.write(json.dumps(paper, ensure_ascii=False) + "\n")

    return result_json


@mcp.tool()
def check_novelty(
    topic: str,
    hypotheses: str,
    session_id: str = "",
) -> str:
    """Assess research novelty by checking overlap with existing academic work.

    Returns a novelty score (0-1), assessment tier, similar papers, and recommendation.

    Args:
        topic: Research topic description
        hypotheses: Hypothesis text or path to a .md file with hypotheses
        session_id: Session ID for context isolation (from research_session_new)
    """
    # If session_id provided, try reading hypotheses from session context
    if session_id and not Path(hypotheses).is_file():
        ctx = get_context_path(session_id)
        hyp_file = ctx / "hypotheses.md"
        if hyp_file.is_file() and not hypotheses.strip():
            hypotheses = str(hyp_file)

    return run_novelty(topic, hypotheses)


@mcp.tool()
def verify_citations(
    bib: str,
    session_id: str = "",
) -> str:
    """Verify BibTeX citations against real academic APIs to detect hallucinated references.

    Uses CrossRef, OpenAlex, arXiv, and Semantic Scholar for four-layer verification.

    Args:
        bib: BibTeX text or path to a .bib file
        session_id: Session ID for context isolation (from research_session_new)
    """
    result_json = run_verify(bib)

    # Persist verification report to session context
    if session_id:
        ctx = get_context_path(session_id)
        report_file = ctx / "citation_verification.json"
        report_file.write_text(result_json, encoding="utf-8")

    return result_json


@mcp.tool()
def detect_domain(
    topic: str,
    session_id: str = "",
) -> str:
    """Detect the research domain from a topic description.

    Returns domain profile with experiment paradigm, standard baselines,
    core libraries, metric types, and domain-specific guidance.

    Args:
        topic: Research topic description
        session_id: Session ID for context isolation (from research_session_new)
    """
    result_json = run_detect(topic)

    # Persist domain profile to session context
    if session_id:
        ctx = get_context_path(session_id)
        profile_file = ctx / "domain_profile.json"
        profile_file.write_text(result_json, encoding="utf-8")

    return result_json


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Research Assistant MCP Server")
    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse"])
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    if args.transport == "sse":
        mcp.run(transport="sse", port=args.port)
    else:
        mcp.run(transport="stdio")
