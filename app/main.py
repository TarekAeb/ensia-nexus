from fastapi import FastAPI

# Routers
from app.api.router import api_router

# Database
from app.core.database import Base, engine

# Import models so SQLAlchemy registers them
from app.infrastructure.database.models import user_model

app = FastAPI(
    title="Research Collaboration API",
    version="1.0.0"
)

# ---------------------------------
# Create tables (for development)
# ---------------------------------

Base.metadata.create_all(bind=engine)

# ---------------------------------
# Register routers
# ---------------------------------

app.include_router(api_router)


# ---------------------------------
# Health check
# ---------------------------------

@app.get("/")
def root():
    return {"message": "API running"}
