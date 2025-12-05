import datetime

from sqlmodel import SQLModel , Field, Relationship

from utils.states import States
from utils.positions import Position
from typing import Optional


class JugadorBase(SQLModel):
    name: str | None = Field(description="player name")
    year: int | None = Field(description="player year")
    nationality:str | None = Field(description="player nationality")
    height:float | None = Field(description="player height")
    weight:float | None = Field(description="player weight")
    dominant_foot:str | None = Field(description="player foot")
    img:Optional[str] = Field(default=None, description="player image")

class Jugador(JugadorBase,table=True):
    id: int | None = Field(default=None, primary_key=True)
    back:int | None = Field(description="player dorsal")
    date: datetime.datetime | None = Field(default_factory=datetime.datetime.now)
    price:int | None = Field(description="player dorsal")
    status: States | None = Field(description="player status", default=States.ACTIVO)
    position:Position | None = Field(description="player position")
    
    
    club_id:int = Field(foreign_key="club.id")
    club: Club = Relationship(back_populates="jugadores")




    

class ClubBase(SQLModel):
    name: str | None = Field(description="club name")
    
    year: int | None = Field(description="club year")

    img:Optional[str] = Field(default=None, description="club image")



class Club(ClubBase,table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    jugadores: list["Jugador"] = Relationship(back_populates="club")
    

class Estadistica():
    pass


class Partido():
    pass


