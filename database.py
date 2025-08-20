# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'fastapi',
    'user': 'postgres',
    'password': 'Mobifly2024'
}

# PostgreSQL Database URL
DATABASE_URL = f"postgresql+asyncpg://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

engine = create_async_engine(
    DATABASE_URL, echo=True, future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# ✅ Fixed: sync-compatible generator function
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
