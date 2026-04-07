# Idea Generation & Novelty Assessment

You are helping the user develop and evaluate research ideas.

User's request: $ARGUMENTS

## Step 0: Session Management

1. Call `research_session_current()` to check active session
2. If no session, call `research_session_new(topic="<topic>")` to create one
3. **Save the `session_id`** and pass to all subsequent tool calls

## Mode Detection

**Mode A — Idea Generation** (vague direction): → Step 1A
**Mode B — Novelty Assessment** (specific idea): → Step 1B

## Step 1A: Guided Idea Generation

Guide through structured ideation:
1. **Gap Identification**: What problems remain unsolved?
2. **Method Transfer**: Techniques from adjacent fields?
3. **Combination**: Methods not yet combined?
4. **Simplification**: Complex approaches made simpler/faster?
5. **Scaling**: Small-scale success untested at large scale?

Formulate each as: Hypothesis + Key assumption + Minimum viable experiment.

## Step 1B: Novelty Assessment

```
check_novelty(topic="<topic>", hypotheses="<text>", session_id="<session_id>")
```

## Step 2: Present Novelty Report

**Novelty Score: X.XX / 1.00** [HIGH/MODERATE/LOW/CRITICAL]
**Recommendation:** [Proceed / Differentiate / Abort]

## Step 3: Refine Hypotheses

```
## H1: [Title]
**Claim**: ... **Method**: ... **Metric**: ... **Novelty**: ...
```

## Step 4: Save Context

Write hypotheses to session context.

## Scoring: 1.0 - max_similarity, penalty for high-citation overlaps. Tiers: high(≥0.7)/moderate(≥0.45)/low(≥0.25)/critical.
