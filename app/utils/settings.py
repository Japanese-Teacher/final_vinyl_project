from pydantic_settings import BaseSettings


class EnvSettings(
    BaseSettings,
    env_file=".env",
):
    postgres_dsn: str
    test_postgres_dsn: str

    class Config:
        env_file = ".env"


def get_env_settings() -> EnvSettings:
    return EnvSettings()
