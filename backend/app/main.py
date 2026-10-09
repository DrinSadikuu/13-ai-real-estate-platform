from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.properties import router as properties_router
from app.core.config import get_settings
from app.core.exceptions import NotFoundError
from app.api.routes.clients import router as clients_router
from app.api.routes.viewings import router as viewings_router
from app.api.routes.client_preferences import router as client_preferences_router
from app.api.routes.agent import router as agent_router


settings = get_settings()

app = FastAPI(
    title=settings.app_name
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


app.include_router(properties_router)
app.include_router(clients_router)
app.include_router(viewings_router)
app.include_router(client_preferences_router)
app.include_router(agent_router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "environment": settings.environment,
    }