import signal
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.routers import generate, sales


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("Shutting down gracefully...")


app = FastAPI(
    title="ラクマネ API",
    description="デジタル商品販売支援システム",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3847"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(sales.router, prefix="/api", tags=["sales"])


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


def handle_sigterm(signum, frame):
    print("Received SIGTERM, initiating graceful shutdown...")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_sigterm)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8291)
