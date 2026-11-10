# DeepSeek-V4.1-Flash setup (Volcengine Ark)

This app uses the official Ark Chat Completions API:

- Model ID: `deepseek-v4-1-flash-261017`
- Base URL: `https://ark.cn-beijing.volces.com/api/v3`
- POST endpoint: `/chat/completions`

## Install and run

1. Copy `.env.example` to `.env` beside `app.py`.
2. Fill `ARK_API_KEY` with your own Ark key. Never commit or share this file.
3. Run `python app.py`.
4. Visit `http://127.0.0.1:8000/api/health`. `mode: live` only means credentials were loaded, not that the provider accepted them.
5. Send a test chat message and confirm the UI shows a live AI response, not demo.

If you receive 404, check model access for your Ark account and the exact model ID. If the model is not available, use the endpoint ID from the Ark console (often `ep-...`) as `AI_MODEL`.

**Security:** A credential was previously pasted into a chat. Rotate it in the Ark console before using the project. Do not upload `.env` to GitHub.

Reference: https://console.volcengine.com/ark/region:cn-beijing/docs/deepseek-v4-1-flash
