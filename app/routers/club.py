from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status,Request
from fastapi.responses import RedirectResponse
from sqlmodel import select

from db import SessionDep
from models import Club, ClubCreate
from supa_impt.supa_bucket import upload_to_bucket

router = APIRouter(prefix="/club", tags=["Club"])

@router.post("/", response_model=Club, status_code=status.HTTP_201_CREATED)
async def create_club(
    request:Request,
    session: SessionDep,
    club_data: ClubCreate, 
    name: str = Form(...),
    year: int = Form(...),
    img: Optional[UploadFile] = File(None)):

    img_url = None
    if img:
        try:
            img_url = await upload_to_bucket(img)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    try:
        new_club = ClubCreate(name=name, year=year, img=img_url)

        club = Club.model_validate(new_club)
        
        session.add(club)
        
        await session.commit()
        
        await session.refresh(club)

    except Exception as e:
        
        raise HTTPException(status_code=400, detail=str(e))

    return RedirectResponse(url=f"/users/{club.id}", status_code=302)
