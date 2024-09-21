from uuid import UUID
from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

from api.dependencies import get_current_user
from api.services.cron.sendNotification import check_out_of_bounds
from .routers import (
    cattles,
    user,
    farms,
    calves,
    annotations,
    vaccines,
    data_analysis,
    financial,
    weight,
)

# Inicializando a aplicação e o scheduler
app = FastAPI()
scheduler = AsyncIOScheduler()

# Incluindo os routers
app.include_router(user.router)
app.include_router(farms.router)
app.include_router(cattles.router)
app.include_router(calves.router)
app.include_router(annotations.router)
app.include_router(vaccines.router)
app.include_router(data_analysis.router)
app.include_router(financial.router)
app.include_router(weight.router)

# Adicionando o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Job agendado para verificar gados fora do terreno
@scheduler.scheduled_job("interval", minutes=0.6)
async def scheduled_check():
    farm_id = UUID("f721300f-f6a9-4d70-b343-82487d070be1")
    await check_out_of_bounds(farm_id)


# Gerenciador de ciclo de vida usando `lifespan`
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código executado na inicialização
    scheduler.start()
    try:
        yield
    finally:
        # Código executado no encerramento
        scheduler.shutdown()


# Atribuindo o gerenciador de ciclo de vida ao FastAPI
app.router.lifespan_context = lifespan


# Endpoints
@app.get("/")
def read_root():
    return {"message": "API is running"}


@app.get("/token", dependencies=[Security(get_current_user)])
async def verify_token():
    return {"message": "Token is valid"}
