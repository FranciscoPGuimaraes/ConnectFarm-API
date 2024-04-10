from fastapi import FastAPI

from .routers import culture

app = FastAPI()

app.include_router(culture.router)

# on root run with:
# python -m uvicorn api.api:app --reload
@app.get("/")
def read_root():
    return {"API": "BaseAPI teste"}