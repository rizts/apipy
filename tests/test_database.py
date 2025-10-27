import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from app.database import Base, get_db
from app.models import Product


# Create an in-memory SQLite database for testing
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()


def test_database_session_creation(db_session):
    """Test that database session is created successfully"""
    assert db_session is not None


def test_get_db_generator():
    """Test the get_db generator function"""
    with patch('app.database.SessionLocal') as mock_session:
        mock_session_instance = mock_session.return_value
        gen = get_db()
        db = next(gen)
        
        # Verify the session was created
        assert db == mock_session_instance
        
        # Now close the generator
        try:
            next(gen)
        except StopIteration:
            pass
        
        # Verify close was called
        mock_session_instance.close.assert_called_once()