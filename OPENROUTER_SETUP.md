# OpenRouter API Setup Guide

## Why OpenRouter?

OpenRouter provides access to multiple AI models through a single API, offering:
- **Cost-effective**: Pay only for what you use, often cheaper than direct API access
- **Multiple models**: Access GPT-3.5, GPT-4, Claude, Llama, and more
- **No rate limits**: Unlike free-tier OpenAI accounts
- **Unified API**: OpenAI-compatible API format

## Getting Your OpenRouter API Key

### Step 1: Create an Account

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Click **"Sign In"** in the top right
3. Sign up with Google, GitHub, or email

### Step 2: Add Credits

1. After signing in, click on your profile (top right)
2. Click **"Keys"** or **"Credits"**
3. Click **"Add Credits"**
4. Add at least $5 (recommended: $10-20 for testing)
5. Complete the payment

### Step 3: Generate API Key

1. Go to [OpenRouter Keys](https://openrouter.ai/keys)
2. Click **"Create Key"**
3. Give it a name (e.g., "Todo App")
4. Copy the API key (starts with `sk-or-v1-...`)
5. **Important**: Save this key securely - you won't see it again!

## Configuring Your Application

### For Local Development

1. Open your `.env` file (or create one from `.env.example`)
2. Add your OpenRouter API key:

```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### For Docker Deployment

1. Open `.env.docker`
2. Replace the placeholder with your key:

```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### For Production (Vercel/Railway/etc.)

Add the environment variable in your deployment platform:

**Vercel:**
1. Go to Project Settings → Environment Variables
2. Add: `OPENROUTER_API_KEY` = `sk-or-v1-your-key-here`

**Railway:**
1. Go to your project → Variables
2. Add: `OPENROUTER_API_KEY` = `sk-or-v1-your-key-here`

## Choosing a Model

The default model is `openai/gpt-3.5-turbo` (fast and cheap).

To change the model, edit `phase-2-web/backend/app/ai_agent/agent.py`:

```python
self.model = "openai/gpt-3.5-turbo"  # Default
```

### Recommended Models

**Budget-friendly:**
- `openai/gpt-3.5-turbo` - Fast, cheap, good for most tasks ($0.50/1M tokens)
- `meta-llama/llama-3.1-8b-instruct` - Very cheap ($0.06/1M tokens)

**High-quality:**
- `openai/gpt-4-turbo` - Best quality ($10/1M tokens)
- `anthropic/claude-3.5-sonnet` - Excellent reasoning ($3/1M tokens)
- `google/gemini-pro-1.5` - Good balance ($1.25/1M tokens)

**Free (with limits):**
- `google/gemini-flash-1.5` - Free tier available
- `meta-llama/llama-3.1-8b-instruct:free` - Free tier

See all models at: https://openrouter.ai/models

## Testing Your Setup

### 1. Start the Backend

```bash
cd phase-2-web/backend
python -m uvicorn app.main:app --reload
```

### 2. Test the Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message": "Create a task to buy groceries"}'
```

### 3. Check Logs

If successful, you should see:
```
INFO: OpenRouter client initialized for AI agent
INFO: TodoAssistant initialized with model: openai/gpt-3.5-turbo
```

## Troubleshooting

### Error: "The specified token is not valid"

**Solution**: Check that your API key is correct and starts with `sk-or-v1-`

### Error: "Insufficient credits"

**Solution**: Add more credits at https://openrouter.ai/credits

### Error: "Rate limit exceeded"

**Solution**: OpenRouter has generous limits, but if you hit them:
1. Wait a few minutes
2. Upgrade your plan
3. Switch to a different model

### Error: "Model not found"

**Solution**: Check the model name at https://openrouter.ai/models and update `agent.py`

## Cost Estimation

Based on typical usage:

**Light usage** (100 messages/day):
- ~$0.50 - $2/month with GPT-3.5-turbo
- ~$0.05 - $0.20/month with Llama

**Medium usage** (500 messages/day):
- ~$2 - $10/month with GPT-3.5-turbo
- ~$0.25 - $1/month with Llama

**Heavy usage** (2000 messages/day):
- ~$10 - $40/month with GPT-3.5-turbo
- ~$1 - $4/month with Llama

## Migration from OpenAI

If you were using OpenAI API before:

1. Your old `OPENAI_API_KEY` is no longer needed
2. The new implementation uses Chat Completions API (not Assistants API)
3. Conversation history is now stored in-memory (consider Redis for production)
4. All functionality remains the same from the user's perspective

## Security Best Practices

1. **Never commit API keys** to git
2. **Use environment variables** for all secrets
3. **Rotate keys regularly** (every 3-6 months)
4. **Monitor usage** at https://openrouter.ai/activity
5. **Set spending limits** in OpenRouter dashboard

## Support

- OpenRouter Docs: https://openrouter.ai/docs
- OpenRouter Discord: https://discord.gg/openrouter
- GitHub Issues: https://github.com/shaziamuhammad/hackathon2_todo/issues
