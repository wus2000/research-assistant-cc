# Experiment Result Analysis

You are helping the user analyze experiment results.

User's request: $ARGUMENTS

## Step 0: Session Management

1. Call `research_session_current()` to check active session
2. **Use `session_id`** for tool calls

## Step 1: Load Context

Read from session: experiment_plan.md, domain_profile.json, hypotheses.md.

## Step 2: Primary Metric Analysis

| Method | Dataset | Metric (mean±std) | Best Seed | Worst Seed |

## Step 3: Statistical Significance

Paired t-test or Bootstrap CI.

## Step 4: Ablation Analysis

| Variant | Metric | Δ from Full |

## Step 5: Failure Analysis + Visualization Recommendations

## Step 6: Summary

Key Results, Limitations, Next Steps.

## Step 7: Citation Verification (Optional)

```
verify_citations(bib="<path>", session_id="<session_id>")
```
