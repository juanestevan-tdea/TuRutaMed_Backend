import pytest
from pydantic import ValidationError

from app.core.config import Settings

REQUIRED = {
    "mysql_url": "mysql+pymysql://u:p@localhost:3306/db",
    "mongo_url": "mongodb://localhost:27017",
    "redis_url": "redis://localhost:6379",
    "gemini_api_key": "test-key",
    "jwt_secret": "a" * 32,
}


def test_missing_jwt_secret_raises(monkeypatch):
    for var in ("JWT_SECRET", "JWT_SECRET_KEY", "SECRET_KEY"):
        monkeypatch.delenv(var, raising=False)
    data = dict(REQUIRED)
    del data["jwt_secret"]
    with pytest.raises(ValidationError):
        Settings(_env_file=None, **data)


def test_cors_origins_csv_parsing():
    settings = Settings(
        _env_file=None,
        cors_origins="http://localhost:5173,http://localhost:3000",
        **{k: v for k, v in REQUIRED.items() if k != "jwt_secret"},
        jwt_secret="b" * 32,
    )
    assert settings.cors_origins == [
        "http://localhost:5173",
        "http://localhost:3000",
    ]


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            "http://localhost:5173,http://localhost:3000",
            ["http://localhost:5173", "http://localhost:3000"],
        ),
        (
            '["http://localhost:5173", "http://localhost:5174"]',
            ["http://localhost:5173", "http://localhost:5174"],
        ),
    ],
)
def test_cors_origins_from_environment(monkeypatch, raw, expected):
    """docker-compose usa CSV; los .env locales pueden usar JSON."""
    monkeypatch.setenv("CORS_ORIGINS", raw)
    settings = Settings(_env_file=None, **REQUIRED)
    assert settings.cors_origins == expected
