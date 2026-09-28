import uuid

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from .config import EXPORTS_DIR
from .schemas import PromptRequest
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf
from .storage import save_comic, load_comic


router = APIRouter()

templates = Jinja2Templates(directory="templates")


def _generate(req: PromptRequest):

    # 1. Generate story outline
    panels = generate_outline(req)

    # 2. Generate detailed story
    panels = generate_story(req, panels)

    # 3. Generate comic images
    image_paths = [
        generate_image(
            p.image_prompt,
            p.panel_number
        )
        for p in panels
    ]

    # 4. Build comic layout
    layout = build_comic_layout(
        panels,
        image_paths
    )

    # 5. Create unique comic ID
    comic_id = uuid.uuid4().hex

    # 6. Create PDF
    pdf_url = save_pdf(
        layout,
        comic_id
    )

    # 7. Store comic information
    payload = {
        "comic_id": comic_id,
        "request": req.model_dump(),
        "layout": layout,
        "pdf_url": pdf_url
    }

    save_comic(
        comic_id,
        payload
    )

    return payload


@router.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate")
async def generate(

    request: Request,

    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),

):

    try:

        req = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style
        )

        result = _generate(req)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context=result
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(exc)
            },
            status_code=500
        )


@router.post("/generate-comic/json")
async def generate_json(req: PromptRequest):

    try:

        return _generate(req)

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


@router.get("/download/{comic_id}")
async def download(comic_id: str):

    comic = load_comic(comic_id)

    if not comic:
        raise HTTPException(
            status_code=404,
            detail="Comic not found"
        )

    pdf_name = comic["pdf_url"].split("/")[-1]

    path = EXPORTS_DIR / pdf_name

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF file not found"
        )

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=pdf_name
    )


@router.get("/export-success/{comic_id}")
async def export_success(
    request: Request,
    comic_id: str
):

    comic = load_comic(comic_id)

    if not comic:
        raise HTTPException(
            status_code=404,
            detail="Comic not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context=comic
    )


@router.get("/test-image")
async def test_image(
    prompt: str = (
        "A brave fox exploring an enchanted "
        "forest, colourful comic book style"
    )
):

    try:

        path = generate_image(
            prompt,
            0
        )

        return {
            "image_path": path,
            "message": "Image generation test completed."
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc