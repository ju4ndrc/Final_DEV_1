
from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status,Request
from fastapi.responses import HTMLResponse, RedirectResponse
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


@router.get("/", response_class=HTMLResponse)
async def get_all_users(request: Request, session: SessionDep):
    result = await session.execute(select(Club))
    clubs = result.scalars().all()
    return templates.TemplateResponse("user_list.html",
                                      {"request": request, "clubs": clubs})


@router.get("/{club_id}", response_class=HTMLResponse)
async def get_one_user(request: Request, club_id: int, session: SessionDep):
    user_db = await session.get(club, club_id)
    if not club_db:
        raise HTTPException(status_code=404, detail="club not found")
    await session.refresh(club_db, ["pets"])
    return templates.TemplateResponse("club_detail.html", {"request": request, "club": user_db})



@router.get("/{club_id}/players", response_class=HTMLResponse)
async def get_user_pets(request: Request, club_id: int, session: SessionDep):
    club = await session.get(club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="club not found")

    await session.refresh(club, ["pets"])
    #pets = club.pets

    return templates.TemplateResponse("club_pets.html", {"request": request, "club":club,"pets": user.pets})