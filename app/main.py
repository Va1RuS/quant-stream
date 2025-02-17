# main.py
import uvicorn

from fastapi import FastAPI
from .api.endpoints import router as api_router

app = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
