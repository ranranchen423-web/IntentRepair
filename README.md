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

## Run locally

1. Open the project folder in VS Code.
2. Start the server:

```powershell
python app.py
```

4. Visit **http://127.0.0.1:8000**. The `/api/health` endpoint reports whether live mode is configured; it does **not** prove the model successfully responded. Send a test message to confirm a live call. Stop the server with `Ctrl+C`.

No third-party Python package installation is required by this version. Remote API usage may incur charges.

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
