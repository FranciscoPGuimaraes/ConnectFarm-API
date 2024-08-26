from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.services.analysis import analyze_health_history, calculate_weaned_calves_ratio

from .routers import cattles, user, farms, calves, annotations, vaccines

app = FastAPI()

app.include_router(user.router)
app.include_router(farms.router)
app.include_router(cattles.router)
app.include_router(calves.router) 
app.include_router(annotations.router)
app.include_router(vaccines.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return

@app.post("/post")
async def post_testing(request: Request):
    post = await request.json()
    return post

@app.get("/analysis/{farm_id}")
async def post_testing(farm_id: str):
    try:
        result = await analyze_health_history(farm_id)
        return result
    except Exception as e:
        raise e
    
    
@app.get("/analysis2/{farm_id}")
async def post_testing2(farm_id: str):
    try:
        result = await calculate_weaned_calves_ratio(farm_id)
        return result
    except Exception as e:
        raise e