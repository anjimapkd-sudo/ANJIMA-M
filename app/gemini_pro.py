import json
from google import genai
from google.genai import types
from .config import settings
from .schemas import PromptRequest, Panel


def generate_story(req: PromptRequest, panels: list[Panel]):
    if settings.demo_mode:
        for panel in panels:
            panel.caption = f"A {req.tone} moment in {req.setting}."
            panel.narration = f"{req.character_name} faces the moment with courage and curiosity."
        return panels
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env or set DEMO_MODE=true.")
    client = genai.Client(api_key=settings.gemini_api_key)
    outline = [p.model_dump() for p in panels]
    prompt = f"""Expand this 5-panel outline into concise comic narration and captions.
Character: {req.character_name}
Tone: {req.tone}
Story prompt: {req.story_prompt}
Outline: {json.dumps(outline, ensure_ascii=False)}

Return ONLY JSON: {{"panels":[{{"panel_number":1,"caption":"...","narration":"..."}}, ...]}}
Rules: exactly 5 panels; preserve panel numbers; 1-2 short sentences for narration; dialogue may be included naturally; keep content family-friendly; do not add image instructions."""
    response = client.models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.85),
    )
    data = json.loads(response.text)
    by_number = {int(p["panel_number"]): p for p in data.get("panels", [])}
    for panel in panels:
        item = by_number.get(panel.panel_number, {})
        panel.caption = str(item.get("caption", ""))
        panel.narration = str(item.get("narration", ""))
    return panels
