from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, projects, tasks

app = FastAPI(
    title="TaskFlow API",
    description="Task and project management REST API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}
