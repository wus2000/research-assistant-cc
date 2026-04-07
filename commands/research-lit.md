# Literature Survey Workflow

You are helping the user conduct a structured literature survey using real academic APIs.

User's request: $ARGUMENTS

## Step 0: Session Management

1. Call `research_session_new(topic="<topic from user's request>")` MCP tool to create an isolated session
2. **Save the returned `session_id`** — you MUST pass it to all subsequent tool calls in this workflow
3. If the user wants to continue an existing session, call `research_session_list()` and use the existing session_id directly

## Step 1: Parse the Query

Extract from the user's request:
- **Search terms**: the core topic keywords
- **Year constraint**: if they mention "recent" or a specific year, use `year_min`
- **Scope**: broad survey vs. targeted search

If the user provides arguments after `/research-lit`, use those as the search query directly.

## Step 2: Search Papers

Call the `search_papers` MCP tool:

```
search_papers(query="<query>", limit=10, year_min=<YYYY>, session_id="<session_id>")
```

Results are automatically saved to the session's `literature.jsonl`.

If few results (<3), try broader terms, different keywords, or remove year constraint.

## Step 3: Present Results

| # | Title | Year | Venue | Citations | Link |
|---|-------|------|-------|-----------|------|

Highlight: >100 citations (foundational), top venues, last 2 years (cutting edge).

## Step 4: Synthesize (Agent)

Invoke the `literature-reviewer` agent for structured analysis:
- Research themes and clusters
- Methodological trends
- Research gaps
- Recommended reading list
- Potential directions

## Step 5: Save Summary

Write topic summary to the session context directory.

## Methodology

Three academic APIs with deduplication: OpenAlex (10K/day) → Semantic Scholar (1K/5min) → arXiv (1/3s).
Dedup: DOI → arXiv ID → fuzzy title. Sorted by citation count desc.
