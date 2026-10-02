import json
from typing import Any, Dict, List

from app.services.config import GEMINI_API_KEY, GEMINI_MODEL


try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


def _fallback_home(data: Dict[str, Any]) -> Dict[str, Any]:

    budget = data.get("budget", 0)

    return {
        "title": "Personalized Home Interior Plan",
        "summary": (
            f"A practical {data.get('style', 'modern')} "
            f"interior plan for your "
            f"{data.get('room_type', 'room')}."
        ),
        "recommendations": [
            {
                "name": "Functional furniture layout",
                "description": (
                    "Choose furniture according to the room size "
                    "and keep enough walking space."
                ),
                "estimated_price": "Within your budget",
                "reason": "Helps use the available space efficiently.",
                "tips": [
                    "Measure the room before buying furniture.",
                    "Prefer multi-purpose furniture for smaller rooms."
                ]
            },
            {
                "name": "Lighting setup",
                "description": (
                    "Use a combination of general lighting "
                    "and focused lighting."
                ),
                "estimated_price": "₹2,000 - ₹8,000",
                "reason": "Creates a comfortable and useful room.",
                "tips": [
                    "Use warm lighting for relaxing areas.",
                    "Use brighter lighting for study/work areas."
                ]
            },
            {
                "name": "Wall and colour plan",
                "description": (
                    f"Use {data.get('colors') or 'neutral colours'} "
                    "with simple decorative elements."
                ),
                "estimated_price": "₹3,000 - ₹15,000",
                "reason": "Creates a visually balanced space.",
                "tips": [
                    "Avoid too many competing colours.",
                    "Use one main colour and one or two supporting colours."
                ]
            }
        ],
        "budget_note": (
            f"Your stated budget is approximately ₹{budget:,.0f}. "
            "Prioritize essential furniture before decoration."
        )
    }


def _fallback_party(data: Dict[str, Any]) -> Dict[str, Any]:

    budget = data.get("budget", 0)

    return {
        "title": "Personalized Party Plan",
        "summary": (
            f"A practical plan for a "
            f"{data.get('event_type', 'party')} "
            f"with approximately "
            f"{data.get('guests', 0)} guests."
        ),
        "recommendations": [
            {
                "name": "Venue arrangement",
                "description": (
                    f"Arrange the {data.get('venue', 'venue')} "
                    "with clear seating, food and activity areas."
                ),
                "estimated_price": "Depends on venue",
                "reason": "Makes movement and guest management easier.",
                "tips": [
                    "Keep food and activity areas separated.",
                    "Keep enough seating for guests."
                ]
            },
            {
                "name": "Theme decoration",
                "description": (
                    f"Use a {data.get('theme', 'simple')} theme "
                    "with coordinated decorations."
                ),
                "estimated_price": "₹3,000 - ₹15,000",
                "reason": "Creates a consistent party atmosphere.",
                "tips": [
                    "Use reusable decorations where possible.",
                    "Keep the decoration within the main budget."
                ]
            },
            {
                "name": "Food planning",
                "description": (
                    f"Plan food according to the guest count "
                    f"and preference: "
                    f"{data.get('food_preference') or 'mixed'}."
                ),
                "estimated_price": "Depends on menu",
                "reason": "Food is one of the largest party expenses.",
                "tips": [
                    "Confirm the guest count before ordering.",
                    "Keep a small buffer for additional guests."
                ]
            }
        ],
        "budget_note": (
            f"Your stated budget is approximately ₹{budget:,.0f}. "
            "Divide the budget between venue, food and decoration."
        )
    }


def _fallback_jewelry(data: Dict[str, Any]) -> Dict[str, Any]:

    budget = data.get("budget", 0)

    return {
        "title": "Personalized Jewelry Plan",
        "summary": (
            f"Jewelry suggestions for a "
            f"{data.get('occasion', 'special occasion')} "
            f"with a {data.get('style', 'simple')} style."
        ),
        "recommendations": [
            {
                "name": "Main jewelry piece",
                "description": (
                    f"Consider a {data.get('metal', 'gold-tone')} "
                    "necklace or statement piece matching the outfit."
                ),
                "estimated_price": f"Up to ₹{budget:,.0f}",
                "reason": "Provides a clear focal point.",
                "tips": [
                    "Match the jewellery scale with the outfit.",
                    "Avoid using too many statement pieces together."
                ]
            },
            {
                "name": "Earrings",
                "description": (
                    "Choose earrings that complement the neckline "
                    "and overall outfit."
                ),
                "estimated_price": "₹500 - ₹5,000",
                "reason": "Earrings can complete the overall look.",
                "tips": [
                    "Choose lightweight earrings for longer events.",
                    "Coordinate the metal finish with other jewellery."
                ]
            },
            {
                "name": "Optional bracelet",
                "description": (
                    "Add a simple bracelet or bangle if it "
                    "does not compete with the main jewelry."
                ),
                "estimated_price": "₹300 - ₹3,000",
                "reason": "Adds a subtle finishing detail.",
                "tips": [
                    "Keep accessories balanced.",
                    "Choose one dominant jewellery style."
                ]
            }
        ],
        "budget_note": (
            f"Your stated budget is approximately ₹{budget:,.0f}."
        )
    }


def _build_prompt(
    planner_type: str,
    data: Dict[str, Any]
) -> str:

    return f"""
You are PocketSmart AI, a practical personal recommendation assistant.

Planner type:
{planner_type}

User information:
{json.dumps(data, indent=2)}

Create useful, realistic recommendations.

Rules:
1. Respect the user's stated budget.
2. Give practical recommendations.
3. Avoid unrealistic prices.
4. Keep the explanation easy to understand.
5. Give 3 to 5 recommendations.
6. Mention estimated prices where possible.
7. Return ONLY valid JSON.
8. Do not use Markdown.
9. Do not add text before or after the JSON.

Required JSON structure:

{{
    "title": "string",
    "summary": "string",
    "recommendations": [
        {{
            "name": "string",
            "description": "string",
            "estimated_price": "string",
            "reason": "string",
            "tips": ["string", "string"]
        }}
    ],
    "budget_note": "string"
}}
"""


def generate_recommendation(
    planner_type: str,
    data: Dict[str, Any]
) -> Dict[str, Any]:

    if not GEMINI_API_KEY or genai is None:

        if planner_type == "home":
            return _fallback_home(data)

        if planner_type == "party":
            return _fallback_party(data)

        return _fallback_jewelry(data)

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        prompt = _build_prompt(
            planner_type,
            data
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        text = response.text.strip()

        result = json.loads(text)

        if "recommendations" not in result:
            raise ValueError(
                "Invalid AI response."
            )

        return result

    except Exception:

        if planner_type == "home":
            return _fallback_home(data)

        if planner_type == "party":
            return _fallback_party(data)

        return _fallback_jewelry(data)