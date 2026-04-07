---
name: research-idea
description: Generate research ideas and assess novelty against existing work. Use when the user wants to brainstorm ideas, evaluate a research direction, or check if an idea is novel.
---

# Idea Generation & Novelty Assessment

You are helping the user develop and evaluate research ideas.

## Mode Detection

**Mode A -- Idea Generation** (user has a vague direction, needs concrete ideas): -> Step 1A
**Mode B -- Novelty Assessment** (user has a specific idea, wants to check novelty): -> Step 1B

## Step 1A: Guided Idea Generation

Load existing context if available:
- Read `tools/research-assistant/context/literature.jsonl` for known papers
- Read `tools/research-assistant/context/current_topic.md` for topic

Guide the user through structured ideation:
1. **Gap Identification**: Based on the literature, what problems remain unsolved?
2. **Method Transfer**: What techniques from adjacent fields could apply here?
3. **Combination**: What existing methods haven't been combined yet?
4. **Simplification**: What complex approaches could be made simpler/faster?
5. **Scaling**: What works at small scale but hasn't been tested at large scale?

For each promising direction, formulate as:
- **Hypothesis**: "If we [method], then [outcome], because [reasoning]"
- **Key assumption**: What must be true for this to work?
- **Minimum viable experiment**: Simplest test to validate/invalidate

## Step 1B: Novelty Assessment

Run the novelty check:
```bash
cd /Users/shangwu/workspace/opensource_software/Claw-AI-Lab
/opt/homebrew/Caskroom/miniforge/base/envs/clawailab/bin/python tools/research-assistant/cli/research_cli.py novelty --topic "<topic>" --hypotheses "<hypothesis text>"
```

## Step 2: Present Novelty Report

**Novelty Score: X.XX / 1.00** [HIGH / MODERATE / LOW / CRITICAL]
**Recommendation:** [Proceed / Differentiate / Abort]

If similar papers found:
| Paper | Year | Similarity | Citations |
|-------|------|-----------|-----------|

**Differentiation guidance** (if score < 0.7):
- What specifically makes your approach different?
- Can you target a different dataset/domain/scale?
- Can you combine existing approach with a novel component?

## Step 3: Refine Hypotheses

Help refine into structured format:
```
## H1: [Concise title]
**Claim**: [What you expect to show]
**Method**: [How you'll show it]
**Metric**: [Primary metric + target value]
**Novelty**: [What's new compared to closest existing work]
```

## Step 4: Save Context

Save hypotheses to `tools/research-assistant/context/hypotheses.md`.
Update `tools/research-assistant/context/current_topic.md` if topic evolved.

## Novelty Scoring Methodology
- Score = `1.0 - max_similarity` across all found papers
- Penalty for high-citation papers (>50 cites) overlapping at >0.4 similarity
- Tiers: high (>=0.7) / moderate (>=0.45) / low (>=0.25) / critical (<0.25)
- If APIs returned <5 papers, score flagged as `insufficient_data`
