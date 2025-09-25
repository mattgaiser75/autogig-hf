import httpx
from typing import Optional
from .config import settings

SYSTEM_PROMPT = "You are a helpful assistant that writes concise, persuasive sales pitches."

# Recommended open models on Hugging Face that generally work with Inference API
HF_MODELS = [
    {"id": "microsoft/Phi-3-mini-4k-instruct", "label": "Phi-3 Mini 4K Instruct"},
    {"id": "mistralai/Mistral-7B-Instruct-v0.2", "label": "Mistral 7B Instruct v0.2"},
    {"id": "meta-llama/Llama-3.1-8B-Instruct", "label": "Llama 3.1 8B Instruct"},
    {"id": "HuggingFaceH4/zephyr-7b-beta", "label": "Zephyr 7B Beta (chat)"},
    {"id": "google/gemma-7b-it", "label": "Gemma 7B IT"},
]

async def _hf_inference(prompt: str, model: str) -> Optional[str]:
    url = f"{settings.HUGGINGFACE_API_BASE.rstrip('/')}/{model}"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"} if settings.HUGGINGFACE_API_KEY else {}
    # Simple chat-style prompt packing for text-generation
    packed = f"""{SYSTEM_PROMPT}

User:
{prompt}

Assistant:
"""
    body = {
        "inputs": packed,
        "parameters": {
            "max_new_tokens": 220,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(url, headers=headers, json=body)
        # HF returns 200 for success; some models may return 503 if loading
        if r.status_code >= 400:
            return None
        data = r.json()
        # Possible shapes:
        # [{"generated_text": "..."}] OR {"error":"Model ... is loading"}
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"]
        # Some community endpoints return dict with "generated_text"
        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]
        return None

async def generate_text(prompt: str, model: Optional[str] = None) -> Optional[str]:
    provider = settings.LLM_PROVIDER.lower()
    model = model or settings.LLM_DEFAULT_MODEL

    if provider == "huggingface":
        return await _hf_inference(prompt, model)

    # Fallbacks (not used by default but kept for compatibility)
    if provider == "ollama":
        url = f"{settings.OLLAMA_BASE.rstrip('/')}/api/chat"
        body = {
            "model": model,
            "messages": [
                {"role":"system","content": SYSTEM_PROMPT},
                {"role":"user","content": prompt}
            ],
            "stream": False
        }
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(url, json=body)
            if r.status_code >= 400:
                return None
            data = r.json()
            return (data.get("message") or {}).get("content") or data.get("response")

    if provider == "openai":
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        url = f"{settings.OPENAI_API_BASE}/chat/completions"
        body = {"model": model or "gpt-4o-mini",
                "messages": [{"role":"system","content":SYSTEM_PROMPT},
                             {"role":"user","content":prompt}]}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=headers, json=body)
            if r.status_code >= 400:
                return None
            data = r.json()
            try:
                return data["choices"][0]["message"]["content"]
            except Exception:
                return None

    if provider == "openrouter":
        headers = {"Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                   "HTTP-Referer": "https://render.com", "X-Title": "AutoGig"}
        url = f"{settings.OPENROUTER_API_BASE}/chat/completions"
        body = {"model": model or "openrouter/auto",
                "messages": [{"role":"system","content":SYSTEM_PROMPT},
                             {"role":"user","content":prompt}]}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=headers, json=body)
            if r.status_code >= 400:
                return None
            data = r.json()
            try:
                return data["choices"][0]["message"]["content"]
            except Exception:
                return None

    # No provider configured
    return None

def heuristic_pitch(opportunity: dict, influencer: dict, style: str = "professional") -> str:
    bullets = [
        f"Project: {opportunity.get('title')}",
        f"Niche/Tone: {influencer.get('niche','')}/{influencer.get('tone','')}",
        f"Why me: Experience aligned with {opportunity.get('title','this project')} and past results.",
        f"Plan: Kickoff → Milestones → QA → Delivery.",
        "Guarantee: On-time delivery, clear communication, and one revision round included.",
        "CTA: Ready to start—can we schedule a quick chat?"
    ]
    return "\n".join(["Hi there,", ""] + [f"• {b}" for b in bullets])
