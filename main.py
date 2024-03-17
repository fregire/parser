from src.app import App
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from dotenv import load_dotenv
from src.settings.postgres_settings import PostgresSettings
import asyncio
from alembic import command
from alembic.config import Config


def run_migrations():
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", PostgresSettings().get_sync_url())
    command.upgrade(alembic_cfg, "head")


async def close():
    print('Closing...')
    await asyncio.sleep(1)


def init_app() -> App:
    postgres_settings = PostgresSettings()
    async_engine = create_async_engine(postgres_settings.get_async_url(), pool_pre_ping=True)
    HUB_URL = 'https://habr.com'
    SLEEP_IN_SECONDS = 600

    return App(engine=async_engine, parse_timeout=SLEEP_IN_SECONDS)


def main():
    load_dotenv()
    run_migrations()
    app = init_app()

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(app.start())
    except KeyboardInterrupt:
        loop.run_until_complete(close())
        if app:
            loop.run_until_complete(app.stop())
    finally:
        print("Program finished")


if __name__ == '__main__':
    main()


