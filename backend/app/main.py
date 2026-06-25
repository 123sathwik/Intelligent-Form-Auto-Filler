import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.api.v1.router import api_router
from app.api.v1.endpoints.document import router as document_router
from app.api.v1.endpoints.preprocessing import router as preprocessing_router
from app.api.v1.endpoints.nlp import router as nlp_router
from app.api.v1.endpoints.standardizer import router as standardizer_router
from app.api.v1.endpoints.ml import router as ml_router
from app.api.v1.endpoints.classification import router as classification_router
from app.api.v1.endpoints.schemas import router as schemas_router
from app.api.v1.endpoints.pipeline import router as pipeline_router
from app.api.v1.endpoints.submit import router as submit_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("autofiller-backend")

# Initialize app
app = FastAPI(
    title="Intelligent Form Auto-Filler API",
    description="Enterprise-grade API service for document OCR, NLP processing, and form mapping.",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Headers", "Multipart/Form-Data", "*"],
)

# Register custom global exception handlers
register_exception_handlers(app)

# Include route versioning namespaces
app.include_router(api_router, prefix="/api/v1")

# Include document upload at root level as well
app.include_router(document_router, tags=["Documents"])

# Include preprocessing at root level as well
app.include_router(preprocessing_router, tags=["Preprocessing"])

# Include NLP at root level as well
app.include_router(nlp_router, tags=["NLP"])

# Include Standardization at root level as well
app.include_router(standardizer_router, tags=["Standardization"])

# Include ML at root level as well
app.include_router(ml_router, tags=["ML"])

# Include Classification at root level as well
app.include_router(classification_router, tags=["Classification"])

# Include Schemas at root level
app.include_router(schemas_router, tags=["Schemas"])

# Include Pipeline at root level
app.include_router(pipeline_router, tags=["Pipeline"])

# Include Submit at root level
app.include_router(submit_router, tags=["Submit"])


# Root Route
@app.get("/", tags=["System"])
async def root():
    return {
        "project": "Intelligent Form Auto Filler",
        "version": "1.0.0",
        "status": "Running",
        "message": "Backend is running successfully.",
        "docs": "/docs"
    }

# Health Check Route
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": "autofiller-backend",
        "version": "1.0.0",
        "debug_mode": settings.DEBUG
    }

@app.on_event("startup")
def startup_event():
    logger.info("Initializing Intelligent Form Auto-Filler API Backend...")
    logger.info(f"Environment: {settings.ENV}")
    logger.info(f"Debug Mode: {settings.DEBUG}")

    # Automatically create folders on startup
    from app.services.document_service import UPLOADS_DIR, TEMP_DIR, OUTPUT_DIR
    for directory in [UPLOADS_DIR, TEMP_DIR, OUTPUT_DIR]:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Successfully verified/created directory: {directory}")
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {str(e)}")

