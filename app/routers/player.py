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


@router.get("/", response_model=list[Jugador], summary="Get all Players from the DB")
async def all_pets(session: SessionDep):
    result = await session.execute(select(Jugador))
    return result.scalars().all()

@router.get("/{jugador_id}", response_model=Jugador)
async def get_one_pet(player_id: int, session: SessionDep):
    pet_db = await session.get(Jugador, player_id)
    if not pet_db:
        raise HTTPException(status_code=404, detail="player not found")
    return pet_db




