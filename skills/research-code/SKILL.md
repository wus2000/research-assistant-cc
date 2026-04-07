---
name: research-code
description: Generate experiment code skeletons with reproducibility and sanity checks. Use when the user wants to implement their experiment.
---

# Experiment Code Assistance

You are helping the user write experiment code based on their experiment plan.

## Step 1: Load Context

Read existing context:
- `tools/research-assistant/context/experiment_plan.md` -- what to implement
- `tools/research-assistant/context/domain_profile.json` -- domain config
- `tools/research-assistant/context/current_topic.md` -- research topic

If no experiment plan exists, ask the user what they want to implement.

## Step 2: Reference Search (Optional)

Search for reference implementations:
```bash
cd /Users/shangwu/workspace/opensource_software/Claw-AI-Lab
/opt/homebrew/Caskroom/miniforge/base/envs/clawailab/bin/python tools/research-assistant/cli/research_cli.py search "<method name> implementation" --limit 5 --sources openalex,arxiv
```

Also use `gh search repos` or `gh search code` for direct GitHub code search.

## Step 3: Code Generation

Generate experiment code skeleton:
```
experiment/
├── config.yaml          # All hyperparameters and paths
├── main.py              # Entry point
├── data.py              # Dataset loading
├── model.py             # Model definition(s)
├── train.py             # Training loop
├── evaluate.py          # Evaluation and metrics
├── baselines/           # Baseline implementations
├── utils/
│   ├── seed.py          # Reproducibility
│   ├── logger.py        # Experiment logging
│   └── metrics.py       # Metric helpers
└── scripts/
    └── run_all.sh       # Full experiment matrix
```

### Code Principles
- Use libraries from domain profile's `core_libraries`
- Follow `code_generation_hints` for domain-specific patterns
- Include proper seed setting for reproducibility
- Log all hyperparameters at experiment start
- Save intermediate results for recovery

## Step 4: Sanity Check Checklist

Before running:
- [ ] All imports resolve correctly
- [ ] Config file has all required fields
- [ ] Data loading works with tiny subset (1-2 samples)
- [ ] Forward pass produces correct output shape
- [ ] Loss computation returns a scalar
- [ ] One training step completes without error
- [ ] Metrics computation matches expected format
- [ ] Results saved to disk properly
- [ ] Random seeds produce deterministic results

## Step 5: Run Script

Generate `scripts/run_all.sh` for the full experiment matrix:
```bash
#!/bin/bash
SEEDS="42 123 456"
for seed in $SEEDS; do
    python main.py --config config.yaml --seed $seed --method proposed
    python main.py --config config.yaml --seed $seed --method baseline1
done
python evaluate.py --results-dir results/ --output analysis.json
```
