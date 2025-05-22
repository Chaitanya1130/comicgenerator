









import os
from enum import Enum
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from Textgen import generate_comic_script
from Imagegen import generate_comic_images

app = FastAPI()

# ----- Enums for dropdowns -----
class ToneOptions(str, Enum):
    funny = "funny and educational"
    serious = "serious and formal"
    lighthearted = "light-hearted"
    adventurous = "adventurous and heroic"

class StyleOptions(str, Enum):
    vibrant = "comic book, vibrant colors, cartoon"
    manga = "manga-style black and white"
    watercolor = "watercolor illustration"
    minimalist = "minimalist line art"

# ----- Request / Response Schemas -----
class ScriptRequest(BaseModel):
    topic: str
    grade_level: str
    comic_tone: ToneOptions = ToneOptions.funny
    character_types: str = "students and teachers"
    number_of_panels: int = 6

class ScriptResponse(BaseModel):
    script: str

class ImageRequest(BaseModel):
    script: str
    topic: str
    grade_level: str

class ImageResponse(BaseModel):
    image_paths: List[str]

class ComicRequest(BaseModel):
    topic: str
    grade_level: str
    comic_tone: ToneOptions = ToneOptions.funny
    character_types: str = "students and teachers"
    number_of_panels: int = 6

class ComicResponse(BaseModel):
    script: str
    image_paths: List[str]

# ----- Endpoints -----
@app.post("/generate_script", response_model=ScriptResponse)
def api_generate_script(req: ScriptRequest):
    try:
        script = generate_comic_script(
            topic=req.topic,
            grade_level=req.grade_level,
            comic_tone=req.comic_tone.value,
            character_types=req.character_types,
            number_of_panels=req.number_of_panels
        )
        return ScriptResponse(script=script)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_images", response_model=ImageResponse)
def api_generate_images(req: ImageRequest):
    try:
        paths = generate_comic_images(
            script=req.script,
            topic=req.topic,
            grade_level=req.grade_level
        )
        return ImageResponse(image_paths=paths)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_comic", response_model=ComicResponse)
def api_generate_comic(req: ComicRequest):
    # 1. generate script
    try:
        script = generate_comic_script(
            topic=req.topic,
            grade_level=req.grade_level,
            comic_tone=req.comic_tone.value,
            character_types=req.character_types,
            number_of_panels=req.number_of_panels
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script generation failed: {e}")

    # 2. generate images
    try:
        paths = generate_comic_images(
            script=script,
            topic=req.topic,
            grade_level=req.grade_level
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {e}")

    return ComicResponse(script=script, image_paths=paths)
