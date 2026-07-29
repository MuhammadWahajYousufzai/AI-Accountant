from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import (
    auth, expenses, income, transactions, accounts, categories,
    reports, audit, dashboard, ai,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        try:
            await conn.execute(text(
                "ALTER TABLE transactions ALTER COLUMN date TYPE VARCHAR(10) USING date::text"
            ))
        except Exception:
            pass
        try:
            await conn.execute(text(
                "ALTER TABLE audit_runs ALTER COLUMN period_start TYPE VARCHAR(10) USING period_start::text"
            ))
            await conn.execute(text(
                "ALTER TABLE audit_runs ALTER COLUMN period_end TYPE VARCHAR(10) USING period_end::text"
            ))
        except Exception:
            pass
    yield
    await engine.dispose()


app = FastAPI(
    title="AI-Powered Accounting & Finance Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if "*" not in origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(expenses.router, prefix="/api/v1")
app.include_router(income.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")
app.include_router(accounts.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(audit.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "AI-Powered Accounting & Finance Assistant API", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
