"""Configuración centralizada del backend TuRutaMed usando pydantic-settings."""

from functools import lru_cache
from typing import Annotated, Literal

from fastapi import Depends
from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # Aplicación
    app_name: str = "TuRutaMed API"
    app_version: str = "2.5.0"
    environment: Literal["dev", "staging", "prod"] = "dev"
    debug: bool = False

    # Bases de datos
    mysql_url: str = Field(
        ...,
        validation_alias=AliasChoices("MYSQL_URL", "MYSQL_URI"),
    )
    mongo_url: str = Field(
        ...,
        validation_alias=AliasChoices("MONGO_URI", "MONGO_URL"),
    )
    mongo_db_name: str = Field(
        default="turutamed_db",
        validation_alias=AliasChoices("MONGO_DB_NAME", "MONGO_DB"),
    )
    redis_url: str = Field(
        ...,
        validation_alias=AliasChoices("REDIS_URL", "REDIS_URI"),
    )

    # Seguridad / JWT
    jwt_secret: str = Field(
        ...,
        min_length=32,
        validation_alias=AliasChoices("JWT_SECRET", "JWT_SECRET_KEY", "SECRET_KEY"),
    )
    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias=AliasChoices("JWT_ALGORITHM", "ALGORITHM"),
    )
    jwt_expire_minutes: int = Field(
        default=30,
        validation_alias=AliasChoices("JWT_EXPIRE_MINUTES", "ACCESS_TOKEN_EXPIRE_MINUTES"),
    )

    # IA (Gemini)
    gemini_api_key: str = Field(
        ...,
        validation_alias=AliasChoices("GEMINI_API_KEY", "GEMINI_KEY"),
    )
    gemini_model: str = Field(
        default="gemini-1.5-flash",
        validation_alias=AliasChoices("GEMINI_MODEL", "GEMINI_MODEL_NAME"),
    )

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:5173"],
        validation_alias=AliasChoices("CORS_ORIGINS", "ALLOWED_ORIGINS"),
    )

    # Rate limiting
    rate_limit_per_minute: int = Field(
        default=60,
        validation_alias=AliasChoices("RATE_LIMIT_PER_MINUTE", "RATE_LIMIT"),
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("mysql_url", "mongo_url", "redis_url", mode="after")
    @classmethod
    def _validate_url(cls, value: str) -> str:
        if "://" not in value:
            raise ValueError("URL inválida: debe incluir esquema (://)")
        return value


@lru_cache
def get_settings() -> Settings:
    """Retorna la instancia cacheada de Settings."""
    return Settings()  # type: ignore[call-arg]


SettingsDep = Annotated[Settings, Depends(get_settings)]
