import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.routers.product import router
from fastapi import FastAPI
from app.models.product_model import Product
from app.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Create a test app with the product router
app = FastAPI()
app.include_router(router, prefix="/products", tags=["products"])
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


def test_create_product_router():
    """Test creating a product through the router"""
    with patch('app.routers.product.database.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Create an actual Product instance and then mock its attributes as needed
        mock_product = Product(
            id=1,
            name="Test Product",
            category="Test Category", 
            price=10.5
        )
        
        # Mock the database operations
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        response = client.post(
            "/products/",
            json={
                "name": "Test Product",
                "category": "Test Category",
                "price": 10.5
            }
        )
        
        assert response.status_code == 200
        # Since the actual database operation will occur, the response will have the created product
        # We can't predict the exact response, but we know it should be successful
        response_data = response.json()
        assert response_data["name"] == "Test Product"
        assert response_data["category"] == "Test Category"
        assert response_data["price"] == 10.5


def test_get_all_products_router():
    """Test getting all products through the router"""
    from app.database import get_db
    from app.routers.product import router
    from fastapi import FastAPI
    
    # Create the app instance that uses the router
    app = FastAPI()
    app.include_router(router, prefix="/products", tags=["products"])
    
    # Create mock objects for query chain
    mock_db = MagicMock()
    mock_base_query = MagicMock()
    mock_offset_query = MagicMock()
    mock_limit_query = MagicMock()
    
    # Set up the query chain
    mock_db.query.return_value = mock_base_query
    mock_base_query.offset.return_value = mock_offset_query
    mock_offset_query.limit.return_value = mock_limit_query
    
    # Mock the methods
    mock_limit_query.all.return_value = [
        Product(id=1, name="Product 1", category="Category 1", price=10.0),
        Product(id=2, name="Product 2", category="Category 2", price=20.0)
    ]
    mock_base_query.count.return_value = 2
    
    # Create a generator function for dependency override
    def override_get_db():
        yield mock_db
    
    # Apply the dependency override
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client for this specific app
    test_client = TestClient(app)
    
    response = test_client.get("/products/")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["total_items"] == 2
    assert len(response_data["items"]) == 2
    assert response_data["items"][0]["name"] == "Product 1"


def test_get_product_by_id_router():
    """Test getting a product by ID through the router"""
    from app.database import get_db
    from app.routers.product import router
    from fastapi import FastAPI
    
    # Create the app instance that uses the router
    app = FastAPI()
    app.include_router(router, prefix="/products", tags=["products"])
    
    # Create mock objects
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_filtered_query = MagicMock()
    
    # Set up query chain
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filtered_query
    
    # Mock the returned product
    mock_product = Product(
        id=1,
        name="Test Product",
        category="Test Category",
        price=10.5
    )
    mock_filtered_query.first.return_value = mock_product
    
    # Create a generator function for dependency override
    def override_get_db():
        yield mock_db
    
    # Apply the dependency override
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client for this specific app
    test_client = TestClient(app)
    
    response = test_client.get("/products/1")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["name"] == "Test Product"


def test_get_product_by_id_not_found():
    """Test getting a product by ID that doesn't exist"""
    with patch('app.routers.product.database.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock query operations
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filtered_query = MagicMock()
        mock_query.filter.return_value = mock_filtered_query
        
        # Return None to simulate not found
        mock_filtered_query.first.return_value = None
        
        response = client.get("/products/999")
        
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Product not found"


def test_update_product_router():
    """Test updating a product through the router"""
    from app.database import get_db
    from app.routers.product import router
    from fastapi import FastAPI
    
    # Create the app instance that uses the router
    app = FastAPI()
    app.include_router(router, prefix="/products", tags=["products"])
    
    # Create mock objects
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_filtered_query = MagicMock()
    
    # Mock the existing product with proper attributes that might be accessed
    mock_existing_product = MagicMock()
    mock_existing_product.id = 1
    mock_existing_product.name = "Old Product"
    mock_existing_product.category = "Old Category"
    mock_existing_product.price = 5.0
    mock_existing_product.image_path = None  # This should be a proper value, not a mock
    
    # Set up query chain
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filtered_query
    mock_filtered_query.first.return_value = mock_existing_product
    
    # Create a generator function for dependency override
    def override_get_db():
        yield mock_db
    
    # Apply the dependency override
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client for this specific app
    test_client = TestClient(app)
    
    response = test_client.put(
        "/products/1",
        json={
            "name": "Updated Product",
            "category": "Updated Category",
            "price": 15.0
        }
    )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Updated Product"
    assert response_data["category"] == "Updated Category"
    assert response_data["price"] == 15.0


def test_update_product_not_found():
    """Test updating a product that doesn't exist"""
    with patch('app.routers.product.database.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock query operations
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filtered_query = MagicMock()
        mock_query.filter.return_value = mock_filtered_query
        
        # Return None to simulate not found
        mock_filtered_query.first.return_value = None
        
        response = client.put(
            "/products/999",
            json={
                "name": "Updated Product",
                "category": "Updated Category",
                "price": 15.0
            }
        )
        
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Product not found"


def test_delete_product_router():
    """Test deleting a product through the router"""
    from app.database import get_db
    from app.routers.product import router
    from fastapi import FastAPI
    
    # Create the app instance that uses the router
    app = FastAPI()
    app.include_router(router, prefix="/products", tags=["products"])
    
    # Create mock objects
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_filtered_query = MagicMock()
    
    # Mock the existing product
    mock_existing_product = MagicMock()
    mock_existing_product.id = 1
    mock_existing_product.name = "Test Product"
    mock_existing_product.category = "Test Category"
    mock_existing_product.price = 10.0
    
    # Set up query chain
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filtered_query
    mock_filtered_query.first.return_value = mock_existing_product
    
    # Create a generator function for dependency override
    def override_get_db():
        yield mock_db
    
    # Apply the dependency override
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client for this specific app
    test_client = TestClient(app)
    
    response = test_client.delete("/products/1")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert response_data["message"] == "Product deleted"


def test_delete_product_not_found():
    """Test deleting a product that doesn't exist"""
    with patch('app.routers.product.database.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock query operations
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filtered_query = MagicMock()
        mock_query.filter.return_value = mock_filtered_query
        
        # Return None to simulate not found
        mock_filtered_query.first.return_value = None
        
        response = client.delete("/products/999")
        
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Product not found"