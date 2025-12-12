from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import db
from app.api import routes
import os

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
origins = ["*"] # Adjust for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup/Shutdown events
@app.on_event("startup")
async def startup_db_client():
    await db.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.disconnect()

# Mount API routes
app.include_router(routes.router, prefix="/api")

# Mount Static API (Frontend)
# We mount static at root "/" but we need to ensure index.html is served.
# Usually FastAPI StaticFiles serves files, but for root "/" to serve index.html we might need a small redirect or configuration.
# Or simpler: Mount /static for assets, and have a root route return index.html
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_dir = os.path.join(base_dir, "static")

if not os.path.isdir(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

from fastapi.responses import FileResponse

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/admin")
async def read_admin():
    return FileResponse(os.path.join(static_dir, "admin.html"))
