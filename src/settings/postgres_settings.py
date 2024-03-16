from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    pg_host: str = Field(validation_alias="PG_HOST", default="localhost")
    pg_port: int = Field(validation_alias="PG_PORT", default=5432)
    pg_username: str = Field(validation_alias="PG_USERNAME", default="postgres")
    pg_password: str = Field(validation_alias="PG_PASSWORD", default="postgres")
    pg_database: str = Field(validation_alias="PG_DATABASE", default="postgres")

    def get_async_url(self):
        return f"postgresql+asyncpg://{self.pg_username}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}"

    def get_sync_url(self):
        return f"postgresql+psycopg2://{self.pg_username}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"
