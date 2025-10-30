# Screen AI Relay on Render

A minimal FastAPI relay that accepts screenshots from the client, performs OCR+analysis using OpenAI Vision models, and sends results to Telegram.

## Deploy to Render

1. Commit/push this repo to GitHub.
2. On Render, create a new Web Service from the repo.
3. Use:
   - Build Command: `pip install -r cloud_server/requirements.txt`
   - Start Command: `uvicorn cloud_server.main:app --host 0.0.0.0 --port $PORT`
4. Set Environment Variables:
   - `OPENAI_API_KEY` – your OpenAI key
   - `TELEGRAM_TOKEN` – your Telegram bot token
   - `CHAT_ID` – your chat id
5. Deploy. The service will be available at `https://screen-frog.onrender.com`.

## Client Configuration

Set the client `config.json` to:
```json
{
  "server_url": "https://screen-frog.onrender.com/process"
}
```

## Telegram Webhook Setup

After deployment, set up the Telegram webhook:
```
https://api.telegram.org/bot<YOUR_TELEGRAM_TOKEN>/setWebhook?url=https://screen-frog.onrender.com/telegram/webhook
```

Replace `<YOUR_TELEGRAM_TOKEN>` with your actual Telegram bot token.

The bot will respond to `/start` with a greeting message.

Now the client can send screenshots from any network, and the cloud relay will handle processing and deliver results to Telegram.
