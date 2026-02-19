"""FastAPI application for BHA Selection Tool.

Run with:
    cd bha_selection
    uvicorn app.backend.main:app --reload --port 8000
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .routes import wells, sections

app = FastAPI(title="BHA Selection Tool", version="0.1.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Log validation errors to stdout so we can debug 422s."""
    body = None
    try:
        body = await request.body()
        body = body.decode("utf-8")[:500]
    except Exception:
        pass
    print(f"  422 Validation Error on {request.method} {request.url}")
    print(f"  Body: {body}")
    for err in exc.errors():
        print(f"  -> {err}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wells.router)
app.include_router(sections.router)

# Serve chart images and other output artifacts as static files
STATIC_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if os.path.isdir(STATIC_ROOT):
    app.mount("/static", StaticFiles(directory=STATIC_ROOT), name="static")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
