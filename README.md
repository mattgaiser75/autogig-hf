# Enhanced Freelance Automation Platform (Render-ready)

A monorepo you can deploy on **Render** with:
- **Web**: Next.js 14 (App Router) + Tailwind + React Query + Zustand + Framer Motion
- **API**: FastAPI + SQLAlchemy + JWT Auth + Celery (Redis) + basic LLM integration
- **Worker**: Celery worker + beat (scheduled tasks)
- **Postgres** for persistence (Render Managed Postgres), **Redis** for queues/cache

> Includes an **AI Influencer Persona** module used by workers when scouting, qualifying, and composing pitches.

---

## 1) One-time: Local quick start

```bash
git clone <your-repo> autogig
cd autogig
cp .env.example .env # (optional for local)
docker compose up --build
# web: http://localhost:3000  api: http://localhost:8000/docs
```

A seed admin is created on first API boot:
- Email: `admin@example.com`
- Password: `admin123`

> Change these in production.

---

## 2) Render deployment

1. Create a **new Postgres** database in Render. Copy its **DATABASE_URL** (prefer the `psycopg` scheme: `postgresql+psycopg://...`).
2. Create a **Redis** in Render and copy its `REDIS_URL`.
3. Create a new **Blueprint** in Render and point it at this repo. Render will read `render.yaml`.
4. Add environment variables to the **autogig-api**, **autogig-worker**, **autogig-beat** services:
   - `DATABASE_URL`: Render Postgres connection string (psycopg format).
   - `REDIS_URL`: Render Redis URL.
   - `JWT_SECRET`: (auto-generated if left blank in web service, but set the same secret across api/worker/beat)
   - (Optional) LLM keys: `OPENAI_API_KEY` or `OPENROUTER_API_KEY` and set `LLM_PROVIDER`.
5. Deploy. The web service will receive `NEXT_PUBLIC_API_URL` automatically from the API service URL.

---

## 3) What’s included

- **Dashboard**: AI insights, pipeline stages, automation status.
- **Opportunities**: Scout stubs (manual trigger), qualification scoring, simple list.
- **Influencers**: Create + auto-generate AI persona (bio, pillars, hooks, schedule) with a single click.
- **Pitch Composer**: Compose a pitch from an opportunity + influencer persona (LLM optional).
- **Compliance/Safety**: Basic policy toggles and audit trail stubs.

> The ML models are stubbed and the Playwright scraping is disabled by default for platform compliance. You can enable it in `api/app/routers/automation.py` once you are ready and in accordance with platform ToS.

---

## 4) Environment variables

See `.env.example` for a full list.

- `DATABASE_URL` (required): Postgres in **psycopg** form: `postgresql+psycopg://user:pass@host:port/db`
- `REDIS_URL` (required)
- `JWT_SECRET` (required)
- `LLM_PROVIDER` (optional): `openai` | `openrouter` | `none`
- `OPENAI_API_KEY`, `OPENAI_API_BASE` (optional)
- `OPENROUTER_API_KEY`, `OPENROUTER_API_BASE` (optional)
- `NEXT_PUBLIC_API_URL` (web only)

---

## 5) Compliance note

Automating interactions with marketplaces and social platforms may violate their Terms. This starter ships **off** by default for automation routines. Enable only if you have permission and accept the risks. Always keep a **human-in-the-loop**.

---

## 6) Extending

- Add real connectors in `api/app/routers/automation.py` using Playwright + proxy rotation.
- Swap LLM providers in `api/app/llm.py` and add provider-specific prompts.
- Add analytics/BI using ClickHouse or your favorite warehouse.

---

Happy shipping!


---

## Open LLMs (Ollama) — Phi-3 Mini, Mistral, Llama3, Quantized
By default the API is set to `LLM_PROVIDER=ollama` and `LLM_DEFAULT_MODEL=phi3:mini`.
To use open models locally:

1. Install Ollama: https://ollama.ai
2. Pull a model, e.g.:
   ```bash
   ollama pull phi3:mini
   # others:
   ollama pull mistral:7b-instruct
   ollama pull llama3:8b-instruct
   ollama pull phi3:mini-4k-instruct-q4_K_M
   ```
3. Ensure Ollama is running at `OLLAMA_BASE` (default `http://localhost:11434`).
4. In the web **Settings** page, pick your model. Persona creation and pitch compose will use it.

> On Render, you can point `OLLAMA_BASE` to an external Ollama host you control.


---

## Hugging Face Inference API (Render-friendly)

This build defaults to **LLM_PROVIDER=huggingface**, so it works great on Render with no extra runtime.

**Setup:**
1. Create a free Hugging Face account and get a token: https://huggingface.co/settings/tokens
2. In Render → Environment for **autogig-api** (and workers if needed), set:
   - `HF_API_TOKEN` = your token
   - (optional) `HF_API_BASE` (defaults to `https://api-inference.huggingface.co/models`)
   - (optional) `LLM_DEFAULT_MODEL` (defaults to `microsoft/Phi-3-mini-4k-instruct`)

**Models:** The Settings page offers a selector with suggested models:
- `microsoft/Phi-3-mini-4k-instruct`
- `mistralai/Mistral-7B-Instruct-v0.2`
- `meta-llama/Meta-Llama-3-8B-Instruct`
- `Qwen/Qwen2-7B-Instruct`

> You can type any other supported repo id in code or set `LLM_DEFAULT_MODEL` to your choice.

**Notes:**
- HF free tier has rate limits and cold starts; for heavier workloads consider upgrading or self-hosting with TGI/vLLM.
- Prompts are wrapped in a generic chat-style template for broad model compatibility.


---

## Hugging Face Inference API (default LLM provider)
This version uses **Hugging Face Inference API** by default for text generation.

### Setup
1. Create a token: https://huggingface.co/settings/tokens
2. Set these env vars (Render → API/Worker/Beat):
   - `LLM_PROVIDER=huggingface`
   - `HF_API_TOKEN=<your token>`
   - `HF_API_BASE=https://api-inference.huggingface.co`
   - `LLM_DEFAULT_MODEL=microsoft/Phi-3-mini-4k-instruct` (or pick from `/llm/models`)
3. In the web app → **Settings**, pick your model (persisted in localStorage).

> If the API returns a 503 (model loading), try again—HF spins up models on demand.
> If LLM calls fail, the system **falls back to a heuristic pitch** so you can keep moving.

### Suggested open models
- `microsoft/Phi-3-mini-4k-instruct` (small, high quality for size)
- `mistralai/Mistral-7B-Instruct-v0.2`
- `HuggingFaceH4/zephyr-7b-beta`
- `Qwen/Qwen2-7B-Instruct`
- `allenai/OLMo-7B-Instruct`



---

## Using Hugging Face Inference API (default)
The API is configured for **Hugging Face Inference API** by default.

**Setup:**
1. Get a free token from: https://huggingface.co/settings/tokens
2. In Render (API/Worker/Beat services), set:
   - `LLM_PROVIDER=huggingface`
   - `HUGGINGFACE_API_BASE=https://api-inference.huggingface.co/models`
   - `HUGGINGFACE_API_KEY=<your_HF_token>`
   - `LLM_DEFAULT_MODEL=microsoft/Phi-3-mini-4k-instruct` (or another from Settings → Model picker)

**How it works:**
- Endpoints `/influencers` (create) and `/opportunities/{id}/compose_pitch` call the HF **text-generation** task.
- We pack a simple chat-style prompt (system + user) and request up to ~220 tokens.

**Swap models easily:**
Use the app **Settings → Choose model** to switch among recommended open models:
- `microsoft/Phi-3-mini-4k-instruct`
- `mistralai/Mistral-7B-Instruct-v0.2`
- `meta-llama/Llama-3.1-8B-Instruct`
- `HuggingFaceH4/zephyr-7b-beta`
- `google/gemma-7b-it`

> If a model is cold-starting, HF may briefly return a loading response. Just retry.
