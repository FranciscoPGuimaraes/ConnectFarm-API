from fastapi import FastAPI

from .routers import user

app = FastAPI()

app.include_router(user.router)

# on root run with:
# python -m uvicorn api.api:app --reload
@app.get("/")
def read_root():
    return