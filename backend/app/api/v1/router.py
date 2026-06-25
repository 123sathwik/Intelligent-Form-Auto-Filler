from fastapi import APIRouter
from app.api.v1.endpoints import document
from app.api.v1.endpoints import preprocessing
from app.api.v1.endpoints import nlp
from app.api.v1.endpoints import standardizer
from app.api.v1.endpoints import ml
from app.api.v1.endpoints import classification
from app.api.v1.endpoints import schemas
from app.api.v1.endpoints import pipeline
from app.api.v1.endpoints import submit

api_router = APIRouter()

# Placeholder route to verify API integration
@api_router.get("/status", tags=["System"])
async def get_api_status():
    return {
        "status": "online",
        "api_version": "v1",
        "environment": "development"
    }

# Document management routers
api_router.include_router(document.router, tags=["Documents"])

# Preprocessing routers
api_router.include_router(preprocessing.router, tags=["Preprocessing"])

# NLP / Entity Extraction routers
api_router.include_router(nlp.router, tags=["NLP"])

# JSON Standardization routers
api_router.include_router(standardizer.router, tags=["Standardization"])

# ML Semantic Mapping routers
api_router.include_router(ml.router, tags=["ML"])

# Classification routers
api_router.include_router(classification.router, tags=["Classification"])

# Schema store routers
api_router.include_router(schemas.router, tags=["Schemas"])

# Pipeline routers
api_router.include_router(pipeline.router, tags=["Pipeline"])

# Submit router
api_router.include_router(submit.router, tags=["Submit"])



