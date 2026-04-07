---
name: research-lit
description: Search and survey academic literature across OpenAlex, Semantic Scholar, and arXiv. Use when the user wants to find related work, survey a research area, or gather papers on a topic.
---

# Literature Survey Workflow

You are helping the user conduct a structured literature survey using real academic APIs.

## Step 1: Parse the Query

Extract from the user's request:
- **Search terms**: the core topic keywords
- **Year constraint**: if they mention "recent" or a specific year, use `--year-min`
- **Scope**: broad survey vs. targeted search for specific methods

If the user provides arguments after `/research-lit`, use those as the search query directly.

## Step 2: Search Papers

Run the academic search CLI tool:

```bash
cd /Users/shangwu/workspace/opensource_software/Claw-AI-Lab
/opt/homebrew/Caskroom/miniforge/base/envs/clawailab/bin/python tools/research-assistant/cli/research_cli.py search "<query>" --limit 10 --year-min <YYYY>
```

If the first search returns few results (<3), try:
1. Broader query terms (remove specific method names)
2. Different keyword combinations
3. Remove year constraint

## Step 3: Present Results

Format the search results as a table:

| # | Title | Year | Venue | Citations | Link |
|---|-------|------|-------|-----------|------|

Highlight:
- Papers with >100 citations (foundational)
- Papers from top venues (NeurIPS, ICML, ICLR, CVPR, etc.)
- Papers from the last 2 years (cutting edge)

## Step 4: Synthesize (Agent)

Invoke the `literature-reviewer` agent to produce a structured analysis:
- Research themes and clusters
- Methodological trends
- Research gaps
- Recommended reading list
- Potential directions

## Step 5: Save Context

After completing the survey:
1. Save search results to `tools/research-assistant/context/literature.jsonl` (one JSON object per line)
2. Update `tools/research-assistant/context/current_topic.md` with the search topic and brief summary

## Methodology Notes

This search uses three academic APIs with automatic deduplication:
- **OpenAlex** (primary): 10K requests/day, indexes most academic sources
- **Semantic Scholar**: Rich citation data, 1K requests per 5 minutes
- **arXiv**: Preprints, 1 request per 3 seconds

Deduplication: DOI -> arXiv ID -> normalized title fuzzy match.
Results sorted by citation count (descending), then year (descending).
