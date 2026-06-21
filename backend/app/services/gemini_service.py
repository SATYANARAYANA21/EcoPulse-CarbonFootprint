"""
Google Vertex AI Gemini integration for personalized carbon reduction insights.

Uses the Vertex AI SDK (google-cloud-aiplatform / vertexai) to call
Gemini 1.5 Flash and generate 3 structured, quantified reduction actions
tailored to the user's actual emission profile.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

import httpx

from app.core.config import get_settings
from app.models.insights import InsightItem

logger = logging.getLogger(__name__)


class GeminiUnavailableError(Exception):
    """Raised when Gemini cannot produce a valid response (network, parse, timeout)."""


def _build_prompt(
    ranked_categories: list[dict[str, Any]],
    breakdown: dict[str, float],
    total_kg: float,
) -> str:
    """Construct the structured prompt for Gemini."""
    category_lines = "\n".join(
        f"  {i + 1}. {item['category'].title()}: {item['kg']} kg CO2e/year "
        f"({item['percentage']}% of total)"
        for i, item in enumerate(ranked_categories)
    )

    return f"""\
You are a carbon footprint reduction expert helping a user reduce their personal CO2e emissions.

USER'S CARBON FOOTPRINT PROFILE:
- Total annual footprint: {total_kg} kg CO2e/year
- Breakdown by category (ranked largest first):
{category_lines}

TASK:
Generate exactly 3 highly personalized, quantified carbon reduction actions for this user.

REQUIREMENTS for each action:
1. Target this user's ACTUAL biggest emission sources (use the ranked list above)
2. Include a SPECIFIC estimated annual CO2e saving in kg (be realistic, not exaggerated)
3. Be ACTIONABLE within 30 days — no vague advice like "be more conscious"
4. Be SPECIFIC — e.g., "Switch daily 15 km petrol commute to train" not just "use less transit"
5. The saving estimate must reflect user's actual numbers (e.g., drive 20k km/year)

RESPONSE FORMAT:
Return ONLY a valid JSON array. No markdown, no explanation, no code fences. Example:
[
  {{
    "category": "transport",
    "action": "Replace daily petrol car commute with transit 4 days per week.",
    "estimated_saving_kg": 1200.0,
    "timeframe": "Achievable within 30 days",
    "priority": 1
  }},
  ...
]

Valid category values: transport, home, diet, consumption
Priority must be 1, 2, or 3 (1 = highest impact)
"""


async def generate_insights_gemini(
    ranked_categories: list[dict[str, Any]],
    breakdown: dict[str, float],
    total_kg: float,
) -> list[InsightItem]:
    """Call Google Gemini API via REST to generate personalized carbon insights.

    Args:
        ranked_categories: Sorted list of {category, kg, percentage} dicts (biggest first).
        breakdown: Per-category kg CO2e dict.
        total_kg: Total annual footprint in kg CO2e.

    Returns:
        List of exactly 3 InsightItem instances.

    Raises:
        GeminiUnavailableError: If Gemini returns an error, invalid JSON, or times out.
    """
    settings = get_settings()
    api_key = getattr(settings, "GEMINI_API_KEY", None)
    if not api_key:
        raise GeminiUnavailableError("GEMINI_API_KEY is not set.")

    try:
        prompt = _build_prompt(ranked_categories, breakdown, total_kg)
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.4,
                "topP": 0.8,
                "maxOutputTokens": 1024,
            }
        }
        
        model_name = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            
        resp_data = response.json()
        raw_text = resp_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        raw_text = raw_text.strip()

        # Strip potential markdown code fences Gemini sometimes adds
        if raw_text.startswith("```"):
            if "\n" in raw_text:
                raw_text = raw_text.split("\n", 1)[1]
            if "```" in raw_text:
                raw_text = raw_text.rsplit("```", 1)[0]
            raw_text = raw_text.strip()

        raw_insights: list[dict[str, Any]] = json.loads(raw_text)

        if not isinstance(raw_insights, list) or len(raw_insights) == 0:
            raise ValueError("Gemini returned empty or non-list JSON")

        # Parse and validate each insight through Pydantic
        items: list[InsightItem] = []
        for idx, raw in enumerate(raw_insights[:3], start=1):
            raw["priority"] = idx  # Normalise priority to 1-3 sequence
            items.append(InsightItem(**raw))

        logger.info("Gemini generated %d insights successfully", len(items))
        return items

    except GeminiUnavailableError:
        raise
    except Exception as exc:
        logger.warning("Gemini unavailable: %s — %s", type(exc).__name__, exc)
        raise GeminiUnavailableError(f"Gemini call failed: {exc}") from exc
