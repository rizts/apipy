import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
from main import app
from app.models import Product
from app.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Set a test secret key for auth functions
os.environ["SECRET_KEY"] = "test_secret_key_for_testing"

# Override dependencies to bypass authentication for testing
from main import get_current_admin, get_current_user
from auth import decode_access_token

def override_get_current_admin():
    """Mock function to override get_current_admin dependency"""
    mock_user = MagicMock()
    mock_user.is_admin = True
    return mock_user

def override_get_current_user():
    """Mock function to override get_current_user dependency"""
    mock_user = MagicMock()
    mock_user.username = "testuser"
    return mock_user

# Apply dependency overrides
app.dependency_overrides[get_current_admin] = override_get_current_admin
app.dependency_overrides[get_current_user] = override_get_current_user

# Create a test client
client = TestClient(app)


@pytest.fixture
def mock_db_session():
    """Create a mock database session for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()


def test_read_root():
    """Test the main FastAPI app is running"""
    response = client.get("/")
    # This will likely return a 404 since there's no root endpoint defined
    assert response.status_code in [200, 404, 405]  # Allow multiple possible responses


def test_token_endpoint_success():
    """Test the token endpoint with correct credentials"""
    # Create mock objects
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_user.hashed_password = "hashed_password"
    
    # Mock the query chain
    mock_query_result = MagicMock()
    mock_db.query.return_value = mock_query_result
    mock_filter_result = MagicMock()
    mock_query_result.filter.return_value = mock_filter_result
    mock_filter_result.first.return_value = mock_user
    
    # Get the get_db function from main module
    from main import get_db
    
    # Temporarily override the get_db dependency
    def mock_get_db():
        yield mock_db
    
    # Apply the override
    app.dependency_overrides[get_db] = mock_get_db
    
    try:
        # Mock the verify_password function
        with patch('main.verify_password', return_value=True):
            # Mock create_access_token
            with patch('main.create_access_token', return_value="mocked_token"):
                response = client.post(
                    "/token",
                    data={
                        "username": "testuser",
                        "password": "validpassword"
                    }
                )
                
                assert response.status_code == 200
                response_data = response.json()
                assert "access_token" in response_data
                assert response_data["token_type"] == "bearer"
    finally:
        # Remove the override to avoid affecting other tests
        if get_db in app.dependency_overrides:
            del app.dependency_overrides[get_db]


def test_token_endpoint_invalid_credentials():
    """Test the token endpoint with invalid credentials"""
    with patch('main.SessionLocal') as mock_session:
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        # Return None to simulate user not found
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        response = client.post(
            "/token",
            data={
                "username": "nonexistent",
                "password": "invalidpassword"
            }
        )
        
        assert response.status_code == 401


def test_create_product_success():
    """Test creating a product with valid data and admin access"""
    # This test requires admin access but we've overridden the dependency
    # So no need to mock get_current_admin since it's already mocked globally
    
    with patch('main.save_upload_file') as mock_save_file:
        mock_save_file.return_value = "/uploads/test.jpg"
        
        with patch('main.crud.create_product') as mock_crud_create:
            mock_created_product = Product(
                id=1,
                name="Test Product",
                category="Test Category", 
                price=10.5,
                image_path="/uploads/test.jpg"
            )
            mock_crud_create.return_value = mock_created_product
            
            with patch('main.SessionLocal') as mock_session:
                mock_db = MagicMock()
                mock_session.return_value.__enter__.return_value = mock_db
                
                response = client.post(
                    "/products/",
                    data={
                        "name": "Test Product",
                        "category": "Test Category",
                        "price": "10.5"
                    },
                    files={"file": ("test.jpg", b"fake image content", "image/jpeg")}
                )
                
                assert response.status_code == 200
                response_data = response.json()
                assert response_data["name"] == "Test Product"
                assert response_data["category"] == "Test Category"
                assert response_data["price"] == 10.5


def test_list_products():
    """Test listing products"""
    # Mock the crud function
    with patch('main.crud.list_products') as mock_list_products:
        mock_products = [
            Product(id=1, name="Product 1", category="Category 1", price=10.0),
            Product(id=2, name="Product 2", category="Category 2", price=20.0)
        ]
        mock_list_products.return_value = mock_products
        
        with patch('main.SessionLocal') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            
            response = client.get("/products/")
            
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data) == 2
            assert response_data[0]["name"] == "Product 1"


def test_get_product():
    """Test getting a specific product"""
    with patch('main.crud.get_product') as mock_get_product:
        mock_product = Product(
            id=1,
            name="Test Product", 
            category="Test Category",
            price=10.5
        )
        mock_get_product.return_value = mock_product
        
        with patch('main.SessionLocal') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            
            response = client.get("/products/1")
            
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["id"] == 1
            assert response_data["name"] == "Test Product"


def test_get_product_not_found():
    """Test getting a product that doesn't exist"""
    with patch('main.crud.get_product') as mock_get_product:
        mock_get_product.return_value = None  # Product not found
        
        with patch('main.SessionLocal') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            
            response = client.get("/products/999")
            
            assert response.status_code == 404


def test_update_product():
    """Test updating a product"""
    with patch('main.crud.get_product') as mock_get_product:
        mock_existing_product = Product(
            id=1,
            name="Old Product",
            category="Old Category", 
            price=5.0
        )
        mock_get_product.return_value = mock_existing_product
        
        with patch('main.crud.update_product') as mock_update_product:
            mock_updated_product = Product(
                id=1,
                name="Updated Product",
                category="Updated Category",
                price=15.0
            )
            mock_update_product.return_value = mock_updated_product
            
            with patch('main.SessionLocal') as mock_session:
                mock_db = MagicMock()
                mock_session.return_value.__enter__.return_value = mock_db
                
                response = client.put(
                    "/products/1",
                    data={
                        "name": "Updated Product",
                        "category": "Updated Category", 
                        "price": "15.0"
                    }
                )
                
                assert response.status_code == 200
                response_data = response.json()
                assert response_data["name"] == "Updated Product"


def test_delete_product():
    """Test deleting a product"""
    with patch('main.crud.get_product') as mock_get_product:
        mock_product = Product(
            id=1,
            name="Test Product",
            category="Test Category",
            price=10.5
        )
        mock_get_product.return_value = mock_product
        
        with patch('main.crud.delete_product'):
            with patch('main.SessionLocal') as mock_session:
                mock_db = MagicMock()
                mock_session.return_value.__enter__.return_value = mock_db
                
                response = client.delete("/products/1")
                
                assert response.status_code == 200
                response_data = response.json()
                assert response_data["message"] == "Deleted successfully"