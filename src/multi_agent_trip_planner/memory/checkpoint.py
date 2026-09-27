import os

from dotenv import load_dotenv
from psycopg import AsyncConnection
from psycopg.rows import dict_row
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver


load_dotenv()


async def create_postgres_checkpointer():
    """
    Create PostgreSQL connection and LangGraph checkpointer.
    """

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is not configured."
        )

    connection = await AsyncConnection.connect(
        database_url,
        autocommit=True,
        row_factory=dict_row
    )

    checkpointer = AsyncPostgresSaver(connection)

    # Create checkpoint tables if required.
    await checkpointer.setup()

    return connection, checkpointer