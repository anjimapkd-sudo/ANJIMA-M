import json
from google import genai
from google.genai import types
from .config import settings
from .schemas import PromptRequest, Panel


def _demo_outline(req: PromptRequest):
    return [
        Panel(panel_number=1, title="The Beginning", scene_description=f"{req.character_name} arrives in {req.setting}.", image_prompt=f"{req.character_name} in {req.setting}, {req.art_style}, establishing comic panel, {req.tone} mood"),
        Panel(panel_number=2, title="A Strange Discovery", scene_description="A mysterious clue changes the journey.", image_prompt=f"{req.character_name} discovering a mysterious clue in {req.setting}, {req.art_style}, comic panel, {req.tone} mood"),
        Panel(panel_number=3, title="The Challenge", scene_description="The main challenge appears and the hero must act.", image_prompt=f"{req.character_name} facing a challenge in {req.setting}, {req.art_style}, dynamic comic panel, {req.tone} mood"),
        Panel(panel_number=4, title="The Turning Point", scene_description="A clever decision turns the situation around.", image_prompt=f"{req.character_name} making a clever decision in {req.setting}, {req.art_style}, dramatic comic panel, {req.tone} mood"),
        Panel(panel_number=5, title="A New Beginning", scene_description="The adventure ends with a memorable new beginning.", image_prompt=f"{req.character_name} celebrating a new beginning in {req.setting}, {req.art_style}, final comic panel, {req.tone} mood"),
    ]


def generate_outline(req: PromptRequest):
    if settings.demo_mode:
        return _demo_outline(req)
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env or set DEMO_MODE=true.")
    client = genai.Client(api_key=settings.gemini_api_key)
    prompt = f"""Create a coherent 5-panel comic outline.
Story prompt: {req.story_prompt}
Main character: {req.character_name}
Setting: {req.setting}
Tone: {req.tone}
Art style: {req.art_style}

Return ONLY valid JSON in this exact shape:
{{"panels":[{{"panel_number":1,"title":"...","scene_description":"...","image_prompt":"..."}}, ...]}}
Rules: exactly 5 panels; panel numbers 1-5; concise but vivid; maintain character and setting continuity; image_prompt must describe composition, characters, environment and style without requesting text inside the image."""
    response = client.models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.9),
    )
    data = json.loads(response.text)
    panels = data.get("panels", [])
    if len(panels) != 5:
        raise RuntimeError("Gemini returned an invalid panel count.")
    return [Panel(**p) for p in panels]
