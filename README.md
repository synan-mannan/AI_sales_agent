# AI-Powered Sales Email Follow-Up Agent

## Overview

Production-ready system for automating sales email responses, intent detection, follow-ups, and meeting scheduling.

**Features**:

- Real-time email ingestion (mock SMTP; easy Gmail API swap)
- AI intent classification & auto-reply generation (OpenAI)
- Automated follow-ups & conversation tracking
- Mock meeting scheduler
- FastAPI dashboard APIs
- SQLite DB (Postgres ready)

## Quick Start

1. ```bash
   cd ai_sales_agent
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env: Add OPENAI_API_KEY or set USE_MOCK_AI=true
   ```

2. **Run API + Scheduler**:

   ```bash
   python run.py
   ```

   - API: http://localhost:8000/docs
   - Mock SMTP: Connect to localhost:1025 (use any email client or `swaks`)

3. **Test Flow**:
   - Send email to mock SMTP (e.g., `swaks --to test@example.com --server localhost:1025`)
   - Check `GET /api/v1/leads`
   - `POST /api/v1/emails/process` with sample payload
   - Wait for scheduler or `GET /api/v1/pending-followups`
   - Test replies/meetings via API docs

## Architecture

See [TODO.md](./TODO.md) for implementation status.

**Modules**:

- `email_ingestion`: Parses incoming emails
- `ai_layer`: Intent & response AI
- `follow_up`: Scheduler logic
- `meeting_scheduler`: Calendar mock
- DB: Leads → Emails → Conversations → Meetings

## Production Deployment

1. Set `DB_URL=postgresql://...`
2. Replace mock email with Gmail API (`google-api-python-client`)
3. Use Celery + Redis for production scheduling
4. Docker: See `docker-compose.yml`

## API Endpoints

- `/api/v1/leads` - Manage leads
- `/api/v1/emails/process` - Process incoming email
- `/api/v1/followups/pending` - View pending FUs
- `/api/v1/meetings/schedule` - Book meetings

## Sample Requests

```bash
# Process email
curl -X POST "http://localhost:8000/api/v1/emails/process" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_email": "lead@example.com",
    "subject": "Pricing inquiry",
    "body": "How much does it cost?"
  }'

# List leads
curl "http://localhost:8000/api/v1/leads"
```

## Testing

```bash
pytest tests/
```

## Environment Vars

See `.env.example`.

## Optional Enhancements

- Gmail API integration
- Google Calendar
- React dashboard
- Rate limiting
- Webhooks for real-time
