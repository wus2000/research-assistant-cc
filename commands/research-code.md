# Experiment Code Assistance

You are helping the user write experiment code.

User's request: $ARGUMENTS

## Step 0: Session Management

1. Call `research_session_current()` to check active session
2. **Use `session_id`** for any tool calls

## Step 1: Load Context

Read from session: experiment_plan.md, domain_profile.json.

## Step 2: Reference Search (Optional)

```
search_papers(query="<method> implementation", limit=5, sources="openalex,arxiv", session_id="<session_id>")
```

## Step 3: Code Generation

Standard skeleton: config.yaml, main.py, data.py, model.py, train.py, evaluate.py, baselines/, utils/, scripts/run_all.sh.

Principles: domain core_libraries, seed reproducibility, logging.

## Step 4: Sanity Check

Imports, forward pass shape, loss scalar, one step, deterministic seeds.

## Step 5: Run Script

Generate run_all.sh for the full experiment matrix.
