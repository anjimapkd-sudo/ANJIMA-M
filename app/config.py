from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    gemini_api_key: str = ""
    hf_api_key: str = ""
    gemini_flash_model: str = "gemini-2.5-flash"
    gemini_pro_model: str = "gemini-2.5-pro"
    hf_image_model: str = "stabilityai/stable-diffusion-xl-base-1.0"
    demo_mode: bool = False
    host: str = "127.0.0.1"
    port: int = 8000
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"
DATA_DIR = BASE_DIR / "data"
for directory in (PANELS_DIR, EXPORTS_DIR, DATA_DIR):
    directory.mkdir(parents=True, exist_ok=True)
