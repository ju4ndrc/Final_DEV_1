from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import routers
from database import get_db
from supabase_client import upload_image_to_supabase

router = APIRouter(tags=["Web Pages"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db), q: str = ""):
    characters = app.routers.player.all_pets(db, q=q)
    return request.app.state.templates.TemplateResponse("index.html", {
        "request": request,
        "characters": characters
    })
