#!/usr/bin/env python3
"""
Test database connection and user authentication
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.db.base import get_db
from app.services.auth_service import AuthService
from app.models.schemas import UserCreate


def test_database_connection():
    """Test database connection and basic operations"""
    print("Testing database connection...")
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Test creating a user
        auth_service = AuthService()
        user_create = UserCreate(
            username="testuser",
            email="test@example.com",
            password="testpassword123"
        )
        
        user = auth_service.create_user(db, user_create)
        print(f"Created user: {user.username} (ID: {user.id})")
        
        # Test authenticating the user
        authenticated_user = auth_service.authenticate_user(db, "testuser", "testpassword123")
        if authenticated_user:
            print("Authentication successful!")
        else:
            print("Authentication failed!")
            
        # Test wrong password
        wrong_auth = auth_service.authenticate_user(db, "testuser", "wrongpassword")
        if not wrong_auth:
            print("Wrong password correctly rejected!")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()
        print("Database test completed!")


if __name__ == "__main__":
    test_database_connection()
