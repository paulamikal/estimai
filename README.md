# EstimAI ⚡

AI-powered project estimator that transforms vague ideas into detailed software proposals through a guided questionnaire — no meetings required.

## Stack
- **Frontend:** SvelteKit + Tailwind CSS
- **Backend:** FastAPI + Python
- **AI:** Groq (llama-3.1-8b-instant) via LangChain
- **Email:** Resend
- **Deploy:** Docker Compose

## Setup

### Backend
```bash
cd backend
cp .env.example .env  # fill in your API keys
uv sync
uv run uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker-compose up --build
```

## Environment Variables
See `backend/.env.example` for required variables.