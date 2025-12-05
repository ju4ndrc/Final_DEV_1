import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

import models
from database import engine
from routers import player, club, match, statistic
from web_routes import pages

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sigmotoa FC")

templates = Jinja2Templates(directory="templates")

app.state.templates = templates

app.include_router(player.router, prefix="/api")
app.include_router(club.router, prefix="/api")
app.include_router(match.router, prefix="/api")
app.include_router(statistic.router, prefix="/api")

app.include_router(pages.router)
