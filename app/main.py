from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from app.core.config import settings

from .v1.api import router as v1_router

def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        root_path='/api')
    
    _app.mount("/static", StaticFiles(directory="static"), name="static")
    
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return _app


app = get_application()

app.include_router(v1_router)

# Pagination
add_pagination(app)