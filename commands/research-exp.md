# Experiment Design Workflow

You are helping the user design rigorous experiments.

User's request: $ARGUMENTS

## Step 0: Session Management

1. Call `research_session_current()` to check active session
2. If no session, ask user to run `/research-lit` or `/research-idea` first
3. **Use the `session_id`** for all tool calls

## Step 1: Load Context

Read context files from the session directory.

## Step 2: Detect Domain

```
detect_domain(topic="<topic>", session_id="<session_id>")
```

## Step 3: Structured Design

Guide using domain profile: Baselines, Metrics, Datasets, Ablation, Statistical Protocol, Compute Budget.

## Step 4: Compile Plan

```markdown
# Experiment Plan: [Title]
## Hypotheses / Methods / Datasets / Metrics / Protocol / Expected Results Table
```

## Step 5: Agent Review

Invoke `experiment-advisor` agent for critical review.

## Step 6: Save Context

Write experiment plan to session context.
