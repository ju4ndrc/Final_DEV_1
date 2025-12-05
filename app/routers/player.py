from fastapi import APIRouter, HTTPException,status
from db import SessionDep
from models import Jugador,JugadorCreate,Club
from sqlmodel import select

router = APIRouter(prefix="/player", tags=["Player"])

@router.post("/create",response_model=Jugador,status_code=status.HTTP_201_CREATED)
async def create_player(new_player:JugadorCreate,session:SessionDep):
    player_data = new_player.model_dump()
    player_db = await session.get(Club, player_data.get("club_id"))
    if not player_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    player = Jugador.model_validate(player_data)
    session.add(player)
    await session.commit()
    await session.refresh(player)
    return player





