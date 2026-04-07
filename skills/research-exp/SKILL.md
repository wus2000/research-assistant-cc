---
name: research-exp
description: Design experiments with domain-aware baselines, metrics, and statistical tests. Use when the user wants to plan how to validate a research hypothesis.
---

# Experiment Design Workflow

You are helping the user design rigorous experiments for their research.

## Step 1: Load Context

Read existing context files:
- `tools/research-assistant/context/hypotheses.md` -- what to test
- `tools/research-assistant/context/current_topic.md` -- research topic
- `tools/research-assistant/context/literature.jsonl` -- known related work

If hypotheses don't exist, ask the user to describe what they want to validate.

## Step 2: Detect Domain

Run domain detection:
```bash
cd /Users/shangwu/workspace/opensource_software/Claw-AI-Lab
/opt/homebrew/Caskroom/miniforge/base/envs/clawailab/bin/python tools/research-assistant/cli/research_cli.py domain --topic "<topic>"
```

This returns: experiment paradigm, standard baselines, metric types, statistical tests, core libraries, and domain-specific guidance.

## Step 3: Structured Design

Guide the user through each component using domain profile defaults:

### Baselines
- At least 2-3 baselines from domain profile's `standard_baselines`
- Include both classic and recent SOTA methods

### Metrics
- **Primary**: The single metric that decides if hypothesis is supported
- **Secondary**: Metrics that capture side effects (speed, memory, fairness)

### Datasets
- Use domain profile's `dataset_guidance` for recommendations
- At least one standard benchmark for comparability

### Ablation Study
- For each novel component, plan a variant without it
- Isolates the contribution of each innovation

### Statistical Protocol
- Number of random seeds (minimum 3, recommend 5)
- Significance test from domain profile's `statistical_tests`
- Paired tests for same data splits

### Compute Budget
- Estimate GPU hours from domain profile's `compute_budget_guidance`

## Step 4: Compile Plan

Produce structured experiment plan:
```markdown
# Experiment Plan: [Title]
## Hypotheses
## Methods (Proposed + Baselines + Ablations)
## Datasets
## Metrics (Primary + Secondary)
## Protocol (Seeds, Splits, Statistical test, Compute estimate)
## Expected Results Table
```

## Step 5: Agent Review

Invoke the `experiment-advisor` agent to critically review the plan.

## Step 6: Save Context

Save to:
- `tools/research-assistant/context/experiment_plan.md`
- `tools/research-assistant/context/domain_profile.json`
