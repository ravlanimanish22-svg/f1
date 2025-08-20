from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import logging
from sqlalchemy import text

from routers import auth, user, book
from database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(title="📚 Book Management API", debug=True, lifespan=lifespan)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Health check
@app.get("/health")
async def health_check():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected", "message": "All systems operational"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail={"status": "unhealthy", "error": str(e)})

# Detailed health
@app.get("/health/detailed")
async def detailed_health_check():
    try:
        health_status = {"status": "healthy", "services": {"database": {"status": "connected", "tables": {}}, "api": {"status": "running", "version": "1.0.0"}}}
        async with engine.begin() as conn:
            tables = ["users", "books"]
            for table in tables:
                try:
                    result = await conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    health_status["services"]["database"]["tables"][table] = {"status": "exists", "record_count": count}
                except Exception as e:
                    health_status["services"]["database"]["tables"][table] = {"status": "error", "error": str(e)}
        return health_status
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        raise HTTPException(status_code=503, detail={"status": "unhealthy", "error": str(e)})

# Routers with correct prefixes
app.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(user.router, prefix="/v1/admin", tags=["Admin"])
app.include_router(book.router, prefix="/v1/books", tags=["Books"])
