from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from sqlalchemy.orm import selectinload
from ..db import SessionDep
from ..models import Club, ClubCreate, ClubUpdate

router = APIRouter()

@router.post("", response_model=Club, status_code=status.HTTP_201_CREATED)
async def create_club(data: ClubCreate, session: SessionDep):
    club = Club(**data.model_dump())
    session.add(club)
    await session.commit()
    await session.refresh(club)
    return club

@router.get("", response_model=list[Club])
async def list_clubs(session: SessionDep):
    stmt = select(Club).options(selectinload(Club.jugadores))
    result = await session.exec(stmt)
    return result.all()

@router.get("/{club_id}", response_model=Club)
async def get_club(club_id: int, session: SessionDep):
    club = await session.get(Club, club_id)
    if not club:
        raise HTTPException(404, "Club no encontrado")
    return club

@router.patch("/{club_id}", response_model=Club)
async def update_club(club_id: int, data: ClubUpdate, session: SessionDep):
    club = await session.get(Club, club_id)
    if not club:
        raise HTTPException(404, "Club no encontrado")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(club, k, v)
    session.add(club)
    await session.commit()
    await session.refresh(club)
    return club

@router.delete("/{club_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_club(club_id: int, session: SessionDep):
    club = await session.get(Club, club_id)
    if not club:
        raise HTTPException(404, "Club no encontrado")
    await session.delete(club)
    await session.commit()
