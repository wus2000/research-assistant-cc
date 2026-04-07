# Research Assistant for Claude Code

AI research assistant plugin that provides academic search, novelty assessment, experiment design, and result analysis directly in Claude Code.

## Features

| Command | Description |
|---------|------------|
| `/research-lit` | Search literature across OpenAlex, Semantic Scholar, arXiv |
| `/research-idea` | Generate ideas + assess novelty against existing work |
| `/research-exp` | Design experiments with domain-aware baselines and metrics |
| `/research-code` | Generate experiment code skeletons |
| `/research-analysis` | Analyze results with statistical tests |

**8 MCP Tools**: search_papers, check_novelty, verify_citations, detect_domain + 4 session management tools.

**2 Agents**: literature-reviewer (synthesis), experiment-advisor (peer review).

**Session Isolation**: Each research topic gets a UUID-tagged session directory. Concurrent sessions in different terminals are safe.

## Prerequisites

```bash
# Python 3.11+ with conda
conda create -n clawailab python=3.11
conda activate clawailab

# Install researchclaw
cd /path/to/Claw-AI-Lab/backend/agent
pip install -e ".[all]"
pip install "mcp[cli]"
```

## Install

1. Add marketplace in Claude Code: `/plugins` → Marketplaces → Add → `YourGitHub/research-assistant-cc`
2. Go to Discover tab → Install `research-assistant`
3. Enable the plugin

Or manually add to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "research-assistant-cc": {
      "source": { "source": "github", "repo": "YourGitHub/research-assistant-cc" }
    }
  }
}
```

## Usage

```
/research-lit vision transformer pruning
/research-idea token merging for efficient ViT
/research-exp
/research-code
/research-analysis
```

## License

MIT
