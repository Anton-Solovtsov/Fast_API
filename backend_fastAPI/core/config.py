from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')
cors_allow_origins = os.getenv("cors_allow_origins")


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_allow_origins: list[str]


def get_settings() -> Settings:

    if DATABASE_URL and cors_allow_origins:
        return Settings(
            DATABASE_URL=DATABASE_URL,
            cors_allow_origins=cors_allow_origins
        )
    raise ValueError('Не верно указан DATABASE_URL или cors_allow_origins')
