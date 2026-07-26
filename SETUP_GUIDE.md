# Harness Autonomous Worker Agent — Demo Setup Guide

## What this demo proves

| Without Agent | With Agent |
|---|---|
| Tests fail → pipeline stops → you fix manually | Tests fail → Agent reads logs → Agent commits fix → Tests pass |

The bug is a single `.upper()` call that corrupts todo text. The Agent finds it, removes it, and pushes the fix — without you touching anything.

---

## Files in this folder

| File | Purpose |
|---|---|
| `todo.py` | Working app (green pipeline) |
| `todo_BROKEN_for_demo.py` | Broken app — copy over `todo.py` to trigger the demo |
| `test_todo.py` | 7 pytest tests the Agent uses to detect and verify the fix |
| `requirements.txt` | `pytest` only |
| `.harness/pipeline.yaml` | CI pipeline with Install → Test → Autofix Agent steps |
| `agents/harness-mcp-connector.yaml` | Reference YAML for the LLM connector |

---

## Part 1 — Local setup and test (do this first)

```bash
cd "Demo 1"
pip install -r requirements.txt
pytest test_todo.py -v
```

All 7 tests should pass (green). Now break it:

```bash
cp todo_BROKEN_for_demo.py todo.py
pytest test_todo.py -v
```

`test_add_item_preserves_case` will fail — this is the bug the Agent will fix.

Restore working code after your local check:

```bash
git checkout todo.py      # if using git
# OR copy the original content back manually
```

---

## Part 2 — GitHub repository

1. Create a new GitHub repo (public or private, your choice).
2. Push all files:

```bash
git init
git add .
git commit -m "Initial demo setup"
git remote add origin https://github.com/<YOU>/<REPO>.git
git push -u origin main
```

---

## Part 3 — Harness connectors (one-time setup, ~15 min)

### 3a. GitHub connector

1. Harness UI → **Project Settings** → **Connectors** → **New Connector**
2. Choose **GitHub**
3. Connection type: **HTTP**
4. URL: `https://github.com/<YOU>/<REPO>`
5. Authentication: **Personal Access Token**
   - GitHub → Settings → Developer settings → Personal access tokens → New token
   - Scopes needed: `repo`, `workflow`
6. Save the token as a **Harness Secret** (Settings → Secrets → New Secret → Text)
7. Paste the secret reference in the connector form
8. Click **Test Connection** — must show green

### 3b. LLM connector (Claude)

1. **Connectors** → **New Connector** → **AI / LLM**
2. Provider: **Anthropic**
3. Model: `claude-sonnet-5`
4. API key: save your Anthropic API key as a Harness Secret first, then reference it here
5. Click **Test Connection** — must show green

---

## Part 4 — Import the pipeline

1. Harness UI → **Pipelines** → **Create Pipeline** → **Import from Git**
2. Point to your repo → file path: `.harness/pipeline.yaml`
3. Open the YAML editor and replace all `<PLACEHOLDER>` values:
   - `<YOUR_PROJECT_ID>` — from your Harness project URL
   - `<YOUR_ORG_ID>` — from your Harness org URL
   - `<YOUR_GITHUB_CONNECTOR_ID>` — the identifier you set in Part 3a
   - `<YOUR_LLM_CONNECTOR_ID>` — the identifier you set in Part 3b
   - `<YOUR_REPO_NAME>` — e.g. `todo-agent-demo`
   - `<YOUR_GITHUB_ORG>` — your GitHub username or org
4. Click **Save**

---

## Part 5 — Install the Autofix Agent from Marketplace

1. Harness UI → left sidebar → **Agent Marketplace** (or search "Agents")
2. Find **Autofix** → click **Install**
3. Select the LLM connector you created in Part 3b
4. Click **Confirm**

---

## Part 6 — Demo day script (5 minutes total)

### Scene 1 — Show the green pipeline (~1 min)

Say: *"Here's the app and tests running normally."*

- Trigger pipeline manually: **Run Pipeline** → confirm `todo.py` is the working version
- Show the pipeline passing all 3 steps (Install, Test, Agent step skipped)

### Scene 2 — Break the code and let the Agent fix it (~4 min)

Say: *"Now I'm going to push broken code — the same mistake a developer might make."*

```bash
cp todo_BROKEN_for_demo.py todo.py
git add todo.py
git commit -m "demo: introduce case bug"
git push
```

The push triggers the pipeline automatically. Walk the audience through what happens on screen:

| What they see | What to say |
|---|---|
| Install step passes | "Dependencies install fine — nothing obviously wrong yet." |
| Test step FAILS | "There it is — `test_add_item_preserves_case` fails. Old world: you'd stop here, read logs, fix manually." |
| Agent step starts | "The Autofix Agent wakes up. It reads the exact same pytest output you just saw." |
| Agent commits a fix | "It identified the `.upper()` call, removed it, and pushed a fix commit to the branch." |
| Pipeline re-triggers | "It re-ran the tests on the fixed code automatically." |
| All tests PASS | "Done. You didn't write a line. The agent did." |

Point to the **audit trail** in the Harness execution view — every action the Agent took is logged.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Test Connection` fails for GitHub | Check token scopes — needs `repo` and `workflow` |
| Agent step not available | Make sure you completed Part 5 (Marketplace install) |
| Agent commits but tests still fail | Check `test_command` in the pipeline YAML matches exactly |
| Pipeline doesn't trigger on push | Enable webhook: Repo Settings → Webhooks → add Harness webhook URL |

---

## Key talking points

- **Every action is audited** — Harness logs what the Agent read, decided, and committed
- **Scoped credentials** — the Agent only has access to the connectors you gave it
- **OPA policies apply** — if your org has branch protection or approval gates, the Agent respects them
- **Model is swappable** — change the connector to switch from Claude to OpenAI or Gemini in seconds
