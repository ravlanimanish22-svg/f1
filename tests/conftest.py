import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app


# SQLite in-memory test DB
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
TestingSessionLocal = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


# Async DB setup/teardown
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db():
    # Create tables before each test
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop tables after test
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Override get_db dependency
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# Test client fixture
@pytest.fixture(scope="function")
def client():
    return TestClient(app)
