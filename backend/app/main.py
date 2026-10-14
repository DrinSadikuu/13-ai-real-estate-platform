from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.agents.graph import create_graph
from app.api.routes.properties import router as properties_router
from app.core.config import get_settings
from app.core.exceptions import NotFoundError, ConflictError
from app.api.routes.clients import router as clients_router
from app.api.routes.viewings import router as viewings_router
from app.api.routes.client_preferences import router as client_preferences_router
from app.api.routes.agent import router as agent_router
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from app.api.routes import documents
from app.core.observability import setup_observability

from contextlib import asynccontextmanager

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Phoenix tracing
    setup_observability()

    async with AsyncPostgresSaver.from_conn_string(
        settings.checkpoint_database_url
    ) as checkpointer:

        await checkpointer.setup()

        app.state.checkpointer = checkpointer
        app.state.graph = create_graph(checkpointer)

        print("PostgreSQL checkpointer connected")
        print("Phoenix observability initialized")

        yield

        print("PostgreSQL checkpointer disconnected")

app = FastAPI(
    title=settings.app_name,
    lifespan = lifespan
)


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(
    request: Request,
    exc: NotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message
        },
    )

@app.exception_handler(ConflictError)
async def conflict_exception_handler(
    request: Request,
    exc: ConflictError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": exc.message,
        },
    )



app.include_router(properties_router)
app.include_router(clients_router)
app.include_router(viewings_router)
app.include_router(client_preferences_router)
app.include_router(agent_router)
app.include_router(documents.router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "environment": settings.environment,
    }