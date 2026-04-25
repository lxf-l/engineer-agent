#!/usr/bin/env python3
"""
Database initialization script
Creates the database and tables for the Engineering AI Agent application.
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.db.base import Base, engine
from app.models.user import User


def init_db():
    """Initialize the database"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    # Ensure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    init_db()
