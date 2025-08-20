#!/usr/bin/env python3
"""
Script to create PostgreSQL database and tables
"""

import asyncio
import asyncpg
from database import DB_CONFIG, Base, engine
from models import User, Book
async def create_database():
    """Create database if it doesn't exist"""
    try:
        # Connect to default postgres database
        conn = await asyncpg.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'
        )
        
        # Check if database exists
        result = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            DB_CONFIG['dbname']
        )
        
        if not result:
            # Create database
            await conn.execute(f"CREATE DATABASE {DB_CONFIG['dbname']}")
            print(f"✅ Database '{DB_CONFIG['dbname']}' created successfully!")
        else:
            print(f"✅ Database '{DB_CONFIG['dbname']}' already exists!")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    return True

async def create_tables():
    """Create tables in the database"""
    try:
        # Create tables using SQLAlchemy
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

async def main():
    """Main function to setup database"""
    print("🚀 Setting up PostgreSQL database...")
    
    # Create database
    if await create_database():
        # Create tables
        await create_tables()
        print("🎉 Database setup completed!")
    else:
        print("❌ Database setup failed!")

if __name__ == "__main__":
    asyncio.run(main())
