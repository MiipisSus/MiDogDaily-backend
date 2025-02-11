
from typing import List, Union

from pydantic import AnyHttpUrl, model_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    DATABASE_URL: str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: float
    
    MEDIA_PATH : str
    HEADSHOT_PATH : str
    
    @model_validator(mode="before")
    @classmethod
    def assemble_cors_origins(cls, values: dict) -> dict:
        cors_origins = values.get("BACKEND_CORS_ORIGINS", [])
        if isinstance(cors_origins, str) and not cors_origins.startswith("["):
            values["BACKEND_CORS_ORIGINS"] = [i.strip() for i in cors_origins.split(",")]
        elif not isinstance(cors_origins, list):
            raise ValueError(f"Invalid CORS origins format: {cors_origins}")
        return values
    
    @model_validator(mode="before")
    @classmethod
    def assemble_static_root(cls, values: dict) -> dict:
        # media
        media_path = values.get("MEDIA_PATH")
        values["HEADSHOT_PATH"] = media_path + values.get("HEADSHOT_PATH")
        
        return values
            
    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow"
    )


def get_settings():
    return Settings()

settings = get_settings()
