from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import init_logging
from app.schemas.common import HealthResponse
from app.services.inference import ModelService


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logging()
    logger = logging.getLogger(__name__)
    app.state.model_service = None
    if settings.model_enabled:
        service = ModelService(
            model_path=settings.model_path,
            device=settings.model_device,
            max_length=settings.model_max_length,
            batch_size=settings.model_batch_size,
        )
        try:
            service.load()
        except ModuleNotFoundError as exc:
            logger.warning(
                "Model enabled but dependency missing (%s). "
                "Set MODEL_ENABLED=false or install requirements-ml.txt.",
                exc,
            )
            service = None
        except Exception as exc:
            logger.exception("Failed to load model, continuing without model: %s", exc)
            service = None
        app.state.model_service = service
    yield


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")


app.include_router(api_router, prefix=settings.api_v1_prefix)
