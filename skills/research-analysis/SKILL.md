---
name: research-analysis
description: Analyze experiment results with statistical tests and visualization guidance. Use when the user has results and needs help interpreting them.
---

# Experiment Result Analysis

You are helping the user analyze and interpret experiment results.

## Step 1: Load Context

Read existing context:
- `tools/research-assistant/context/experiment_plan.md` -- expected metrics and baselines
- `tools/research-assistant/context/domain_profile.json` -- domain-specific analysis hints
- `tools/research-assistant/context/hypotheses.md` -- what was being tested

Also ask the user to provide or point to their results data.

## Step 2: Primary Metric Analysis

Compile the main comparison table:
| Method | Dataset | Metric (mean +/- std) | Best Seed | Worst Seed |

Key findings:
- Which method achieves best primary metric?
- How much does proposed method improve over strongest baseline?
- Is improvement consistent across datasets/seeds?

## Step 3: Statistical Significance

**Paired t-test** (default for ML comparison):
```python
from scipy import stats
t_stat, p_value = stats.ttest_rel(proposed_scores, baseline_scores)
```

**Bootstrap CI** (when distribution is non-normal):
```python
import numpy as np
def bootstrap_ci(data, n_bootstrap=10000, ci=0.95):
    means = [np.mean(np.random.choice(data, size=len(data))) for _ in range(n_bootstrap)]
    return np.percentile(means, [(1-ci)/2*100, (1+ci)/2*100])
```

## Step 4: Ablation Analysis

| Variant | Metric | Delta from Full Model |

- Which component contributes most?
- Components that don't help? (candidates for removal)
- Surprising interactions?

## Step 5: Failure Analysis

- On which examples/subsets does the method underperform?
- Systematic patterns in failures?
- What does this suggest about limitations?

## Step 6: Visualization Recommendations

| Purpose | Chart Type | Tool |
|---------|-----------|------|
| Method comparison | Bar chart with error bars | matplotlib |
| Training dynamics | Line plot (loss vs. epoch) | matplotlib |
| Ablation contributions | Grouped bar chart | matplotlib |
| Per-sample analysis | Scatter plot or heatmap | seaborn |
| Statistical significance | Box plot or violin plot | seaborn |

Provide ready-to-use matplotlib code for the most important chart.

## Step 7: Summary

```markdown
## Key Results
1. [Main finding -- does hypothesis hold?]
2. [Secondary finding]
3. [Surprising observation]

## Limitations
## Next Steps
```

## Step 8: Citation Verification (Optional)

If the user has a paper draft with citations:
```bash
cd /Users/shangwu/workspace/opensource_software/Claw-AI-Lab
/opt/homebrew/Caskroom/miniforge/base/envs/clawailab/bin/python tools/research-assistant/cli/research_cli.py verify --bib "<path_to_references.bib>"
```
