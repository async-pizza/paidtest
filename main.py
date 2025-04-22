import logging

from fastapi import FastAPI

from apps.calls.views import router as calls_router
from apps.users.views import router as users_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(docs_url="/api/swagger/", openapi_url="/api/openapi.json")
app.include_router(users_router)
app.include_router(calls_router)


@app.get("/health/")
def health() -> str:
    return "i'm alive"
