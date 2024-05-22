from contextlib import asynccontextmanager
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.dependencies import get_content_service
from src.repositories.meili_search_repository import MeiliSearchRepository

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from .api.routers import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    content_service = get_content_service()
    posts = await content_service.get_posts()
    print("Update meili documents")
    MeiliSearchRepository.update_documents([post.model_dump() for post in posts])
    yield


app = FastAPI( title="С тобой | АПИ документация", lifespan=lifespan) 


@app.get("/")
def index():
    return {"Hello": "World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3010", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
)

for router in routers:
    app.include_router(router)
