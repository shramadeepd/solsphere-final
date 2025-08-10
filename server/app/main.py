from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route import machines, export
from database import init_db
from config import settings

app = FastAPI(title="System Utility Backend")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = settings.API_PREFIX.rstrip("/")
app.include_router(machines.router, prefix=api_prefix, tags=["machines"])
app.include_router(export.router, prefix=api_prefix, tags=["export"])


@app.get("/")
def root():
    return {"status": "ok", "api_prefix": api_prefix}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
    