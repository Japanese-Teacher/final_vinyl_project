from pydantic_settings import BaseSettings


class EnvSettings(
    BaseSettings,
    env_file=".env",
):