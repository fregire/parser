from src.app import App
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from dotenv import load_dotenv
from src.settings.postgres_settings import PostgresSettings
import asyncio


async def close():
    print('Closing...')
    await asyncio.sleep(1)


def main():
    load_dotenv()
    postgres_settings = PostgresSettings()
    async_engine = create_async_engine(postgres_settings.get_async_url(), pool_pre_ping=True)
    HUB_URL = 'https://habr.com'
    SLEEP_IN_SECONDS = 600

    loop = asyncio.get_event_loop()

    try:
        app = App(engine=async_engine, hub=HUB_URL, parse_timeout=SLEEP_IN_SECONDS)
        loop.run_until_complete(app.start())
    except KeyboardInterrupt:
        loop.run_until_complete(close())
        if app:
            loop.run_until_complete(app.stop())
    finally:
        print("Program finished")


if __name__ == '__main__':
    main()


