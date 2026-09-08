from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.config import settings
from app.database import Base, engine
from app.routers import admin, billing, reports

# Setup SQLite Database structure automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend counter retail and storage engine for Guru Pooja master book events.",
    version="1.0.0"
)

# Attach API endpoints directly into routing tables
app.include_router(admin.router)
app.include_router(billing.router)
app.include_router(reports.router)

@app.get("/", include_in_schema=False)
def counter_screen():
    return FileResponse("app/templates/index.html")

@app.get("/api/status")
def root_status_check():
    return {"status": "online", "system": settings.PROJECT_NAME}
