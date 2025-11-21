import os
import json
from typing import Dict, Any, List

import requests
from dotenv import load_dotenv

from .schemas import CalorieAnalysisRequest

# Load environment variables from backend/.env
load_dotenv()


def _extract_text_from_candidates(data: Dict[str, Any]) -> str:
    """
    Safely extract model text from Gemini generateContent response.
    Handles cases where content.parts may be missing.
    """
    candidates: List[Dict[str, Any]] = data.get("candidates", [])
    if not candidates:
        return ""

    content = candidates[0].get("content", {})
    parts = content.get("parts", [])

    texts: List[str] = []
    for p in parts:
        if isinstance(p, dict) and "text" in p:
            texts.append(str(p["text"]))

    return "\n".join(texts).strip()


def analyze_calories_with_gemini(req: CalorieAnalysisRequest) -> Dict[str, Any]:
    """
    Call Google's Gemini API to estimate calories/macros from the
    text description + basic image features.

    Uses REST endpoint (AI Studio / Gemini API):
      https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key=API_KEY

    We explicitly turn OFF "thinking" using thinkingBudget=0 so that
    the model doesn't burn all tokens on hidden reasoning and return
    no visible text. :contentReference[oaicite:1]{index=1}
    """

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Create a .env file with your Gemini API key."
        )

    # Supported alias for current flash model in v1beta
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-flash-latest:generateContent"
        f"?key={api_key}"
    )

    system_prompt = (
        "You are a nutrition assistant. The user uploads a picture of food and a short "
        "text description. You also receive some basic computer vision features. "
        "Estimate an approximate calorie count and macronutrients. Be conservative and "
        "avoid medical language. Output a JSON object with keys: "
        "{total_calories (number), macros (object with protein_g, carbs_g, fats_g), "
        "reasoning (short explanation), suggestions (1-3 bullet suggestions)}."
    )

    user_prompt = (
        f"{system_prompt}\n\n"
        f"User description of dish: {req.description}\n\n"
        "Basic image features:\n"
        f"- width: {req.image_features.get('width')}\n"
        f"- height: {req.image_features.get('height')}\n"
        f"- avg_color_rgb: {req.image_features.get('avg_color_rgb')}\n"
        f"- brightness: {req.image_features.get('brightness')}\n"
        f"- heuristic_dish_hint: {req.image_features.get('dish_hint')}\n\n"
        "Now estimate calories and macros and respond ONLY with JSON. "
        "Do not include any markdown or extra text."
    )

    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": user_prompt},
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 256,
            # 🔑 Turn OFF thinking so we get normal text output,
            # instead of using all tokens on hidden thoughts. :contentReference[oaicite:2]{index=2}
            "thinkingConfig": {
                "thinkingBudget": 0
            },
        },
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=60)
    except requests.RequestException as e:
        # Network / SSL / connection errors
        raise RuntimeError(f"Error calling Gemini API: {e}") from e

    if response.status_code != 200:
        # Surface the exact error body so you can see 401/403/400 details
        raise RuntimeError(
            f"Gemini API error {response.status_code}: {response.text}"
        )

    data = response.json()

    # Robustly extract text from candidates; don't assume parts[0].text exists.
    content_text = _extract_text_from_candidates(data)

    if not content_text:
        # No visible text, even though request succeeded
        # Return a graceful fallback instead of crashing.
        raw = json.dumps(data)[:500]
        return {
            "total_calories": None,
            "macros": None,
            "reasoning": "Model returned no visible text output.",
            "suggestions": [
                "Try again with a shorter description.",
                "If the issue persists, lower the complexity of the prompt.",
            ],
            "raw_response": raw,
            "model_name": data.get("modelVersion", "gemini-flash-latest"),
            "image_features": req.image_features,
        }

    parsed: Dict[str, Any] = {}
    try:
        parsed = json.loads(content_text)
    except json.JSONDecodeError:
        # If the model didn't return valid JSON, fall back to wrapping raw text
        parsed = {
            "total_calories": None,
            "macros": None,
            "reasoning": "Model did not return valid JSON.",
            "suggestions": [content_text],
            "raw_response": content_text,
        }
    else:
        parsed.setdefault("raw_response", content_text)

    parsed.setdefault("model_name", data.get("modelVersion", "gemini-flash-latest"))
    parsed["image_features"] = req.image_features

    return parsed
