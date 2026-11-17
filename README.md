# IntentRepair — AI-Assisted Clarification for Chatbot Misunderstandings

**README prose word count:** 738 (excluding code blocks and commands; approximate Markdown word count)

## Overview

IntentRepair is a local web-based research prototype exploring how visible, context-sensitive clarification options may help non-expert users recover when an AI chatbot misunderstands their request. It builds on an Assignment 1 literature review about ambiguous user intent. Day-trip planning was the original example, but the latest prototype also supports general chat prompts through an external language model.

The central interaction is: **ask a question → receive a response → select “Refine your request” → review AI-generated clarification options → choose an option → receive a revised response**. The user remains in control of whether to refine an answer.

## Project status

| Component | Status | Notes |
|---|---|---|
| Browser chat interface | Implemented | Text input, response display and conversation UI. |
| Live language-model integration | Implemented (requires configuration) | Server-side calls via Volcengine Ark; successful live requests must be verified using the reviewer's own credentials. |
| Dynamic clarification | Implemented (requires live AI) | `/api/clarify` requests one question and 2–4 context-specific options from the model. |
| User-selected revision | Implemented | The selected option is submitted as a follow-up request. |
| Initial ambiguity detection | Rule-based | Limited keyword matching; **not** an LLM confidence score. |
| Offline mode | Simulated | Restricted illustrative answers; dynamic AI options are unavailable. |
| User study and measured usability gains | Not completed | No claim of demonstrated improvement in user outcomes. |

## Technology stack

- **Python 3.10+** and standard-library `http.server`: local server and JSON API endpoints.
- **HTML, CSS and vanilla JavaScript**: chat interface and interactive refinement panel.
- **DeepSeek-V4.1-Flash via Volcengine Ark**: live answer generation and context-sensitive clarification suggestions.
- **Python `unittest`**: local automated tests for core behaviour and error handling.

## Run Locally

### Requirements

- Python 3.10 or later
- Internet access for live AI requests
- A Volcengine Ark API key with access to the configured DeepSeek model
- Visual Studio Code or another terminal environment

### Step 1 — Clone the Repository

Open PowerShell and run:

```powershell
git clone https://github.com/ranranchen423-web/IntentRepair.git
cd IntentRepair
```

### Step 2 — Configure the AI Provider

Create a `.env` file in the project root directory, alongside `app.py`.

If `.env.example` is available, copy it using:

```powershell
Copy-Item .env.example .env
```

Otherwise, create the file manually:

```powershell
notepad .env
```

Add the following configuration:

```env
ARK_API_KEY=YOUR_OWN_ARK_API_KEY
AI_MODEL=deepseek-v4-1-flash-261017
AI_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
AI_MODE=live
```

Replace `YOUR_OWN_ARK_API_KEY` with your personal Ark API key.

The model must be available to your Ark account. If the model identifier is not supported, use the authorised inference endpoint ID provided in the Ark console.

**Security:** Keep `.env` private. Never commit API keys to GitHub or include them in screenshots, reports or shared files. The repository's `.gitignore` excludes `.env`.

### Step 3 — Start the Application

Run:

```powershell
python app.py
```

Open the following address in your browser:

http://127.0.0.1:8000

The application should display `LIVE AI CONNECTED` when valid-looking credentials are loaded. This indicator confirms configuration only, not successful communication with the external model.

### Step 4 — Verify the Live AI Connection

Open:

http://127.0.0.1:8000/api/health

The response should include:

```json
{
  "status": "ok",
  "mode": "live",
  "model": "configured"
}
```

Next, send the following test message:

`Help me learn Python.`

Check that the AI generates a relevant response.

Then click **Refine your request**. The system should generate context-specific clarification options. Select one and click **Update response** to verify the revised answer.

If the provider returns an error, check the API key, account permissions, available model ID and request quota.

### Demo Mode and Limitations

Without a configured API key, the application uses a limited offline simulation. Dynamic AI-generated clarification requires a live model connection.

The prototype is intended for local academic evaluation and does not require deployment to a public server.

No third-party Python packages are required. API requests may incur charges.

Stop the application by pressing `Ctrl+C` in the terminal.

## Test and inspect

```powershell
python -m unittest discover -s tests -v
```

Suggested manual scenarios:

1. **Clear request:** “Suggest a quiet hiking trip near Birmingham.” Check the response and whether any warning is appropriate.
2. **Ambiguous request:** “Suggest a day trip.” Open **Refine your request** and inspect the generated alternatives.
3. **Different domain:** “Help me learn Python.” Check that clarification options relate to learning or coding, rather than fixed travel categories.
4. **Correction:** “I do not want a city trip.” Check that the revision respects this constraint.


## Development record

| Stage | Change and reason | Evidence to inspect |
|---|---|---|
| A1 / Labs | Identified misunderstood intent and sketched normal, failure and recovery interactions. | Literature review, earlier storyboards and `01_SPEC.md`. |
| Initial prototype | Added a runnable chat UI, rule-based ambiguity handling and fixed refinement options to demonstrate the interaction loop. | `app.py`, `intent_engine.py`, `static/`. |
| Live AI integration | Added server-side model calls because the offline demo repeatedly produced unrelated preset answers. | `ai_service.py`, `SETUP_DEEPSEEK.md`. |
| Provider change | Moved from an unsuccessful Doubao configuration to DeepSeek on Ark after API errors. | Configuration guidance and provider-error tests. |
| Dynamic refinement | Replaced fixed hiking/budget/distance choices with model-generated, conversation-specific suggestions. | `/api/clarify`, `static/app.js`, `tests/test_dynamic_refine.py`. |

These are development stages, **not** a claim that separate Git commits already exist. Refer to the actual submitted commit ID or release in the A2 report.

## AI assistance and verification

**ChatGPT** was used to help draft and revise application code. 
**DeepSeek-V4.1-Flash** is the model configured for runtime responses and clarification generation. 

## Additional materials

See `docs/SYSTEM_DIAGRAM.md`, `docs/STORYBOARDS.md`, `docs/TEST_RECORD.md` and `docs/architecture.png` for supporting artefacts. Update diagrams and storyboards to match the final running version, clearly labelling implemented, simulated and planned elements.

## Limitations

The server is intended for local use on `127.0.0.1`, not public deployment. Live prompts are sent to the external provider. Model suggestions may be inaccurate, and the prototype has not established that the interface reduces misunderstanding or task-completion time.
