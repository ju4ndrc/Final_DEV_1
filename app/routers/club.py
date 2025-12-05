from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from db import get_session
from models import Club, ClubCreate, ClubUpdate

router = APIRouter()

@router.post("", response_model=Club, status_code=status.HTTP_201_CREATED)
def create_club(data: ClubCreate, session: Session = Depends(get_session)):
    club = Club(**data.model_dump())
    session.add(club)
    session.commit()
    session.refresh(club)
    return club

@router.get("", response_model=list[Club])
def list_clubs(session: Session = Depends(get_session)):
    # Carga jugadores del club
    result = session.exec(
        select(Club).options(selectinload(Club.jugadores))
    )
    return result.all()

@router.get("/{club_id}", response_model=Club)
def get_club(club_id: int, session: Session = Depends(get_session)):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(404, "Club no encontrado")
    session.refresh(club)
    return club

@router.patch("/{club_id}", response_model=Club)
def update_club(club_id: int, data: ClubUpdate, session: Session = Depends(get_session)):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(404, "Club no encontrado")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(club, k, v)
    session.add(club)
    session.commit()
    session.refresh(club)
    return club

@router.delete("/{club_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_club(club_id: int, session: Session = Depends(get_session)):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(404, "Club no encontrado")
    session.delete(club)
    session.commit()
