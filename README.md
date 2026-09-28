# ComicCraft - AI Comic Story Creator

FastAPI + Jinja2 + Gemini + Hugging Face image generation + FPDF2.

## Features
- Five-panel structured comic outline
- AI narration and captions
- AI-generated illustrations through Hugging Face Inference API
- PDF export
- Browser UI
- JSON API
- Demo mode for testing without AI keys

## Run on Windows
```powershell
cd ComicCraft
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```
Edit `.env` and add your keys. For a no-key test, use `DEMO_MODE=true`.

Start:
```powershell
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs
Health: http://127.0.0.1:8000/health

## Run on macOS/Linux
```bash
cd ComicCraft
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## JSON API example
POST `/generate-comic/json` with:
```json
{"story_prompt":"A brave fox explores an enchanted forest","character_name":"Lumi","setting":"Enchanted forest","tone":"Funny","art_style":"Comic book"}
```

## Notes
- `DEMO_MODE=true` uses local placeholder illustrations and template story content, so you can verify the complete web/PDF workflow without API keys.
- For real text generation set `GEMINI_API_KEY`.
- For real image generation set `HF_API_KEY`.
- Gemini and image model names are configurable in `.env`.
