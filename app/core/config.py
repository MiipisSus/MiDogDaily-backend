
from typing import List, Union

from pydantic import AnyHttpUrl, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    DATABASE_URL: str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: float
    
    @model_validator(mode="before")
    @classmethod
    def assemble_cors_origins(cls, values: dict) -> dict:
        cors_origins = values.get("BACKEND_CORS_ORIGINS", [])
        if isinstance(cors_origins, str) and not cors_origins.startswith("["):
            values["BACKEND_CORS_ORIGINS"] = [i.strip() for i in cors_origins.split(",")]
        elif not isinstance(cors_origins, list):
            raise ValueError(f"Invalid CORS origins format: {cors_origins}")
        return values
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"
        

class TestSettings(Settings):
    DATABASE_URL: str
    
    class Config:
        env_file = ".env.test"

def get_settings():
    import os
    if os.getenv("TESTING"):
        return TestSettings()
    return Settings()

settings = get_settings()
