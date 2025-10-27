import pytest
from unittest.mock import MagicMock, patch
from app.crud import (
    create_product, 
    list_products, 
    get_product, 
    update_product, 
    delete_product
)
from app.models import Product


def test_create_product():
    """Test creating a product"""
    # Mock database session
    mock_db = MagicMock()
    mock_product = Product(
        id=1,
        name="Test Product",
        category="Test Category",
        price=10.5,
        image_path="/path/to/image.jpg"
    )
    
    # Configure the mock to return our test product
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_product_instance = MagicMock()
    mock_product_instance.id = 1
    mock_product_instance.name = "Test Product"
    mock_product_instance.category = "Test Category"
    mock_product_instance.price = 10.5
    mock_product_instance.image_path = "/path/to/image.jpg"
    
    with patch('app.crud.Product', return_value=mock_product_instance):
        result = create_product(
            mock_db, 
            "Test Product", 
            "Test Category", 
            10.5, 
            "/path/to/image.jpg"
        )
        
        # Verify the result
        assert result.name == "Test Product"
        assert result.category == "Test Category"
        assert result.price == 10.5
        
        # Verify database operations were called
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()


def test_list_products():
    """Test listing products"""
    # Mock database session
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    
    # Mock products
    mock_products = [
        Product(id=1, name="Product 1", category="Category 1", price=10.0),
        Product(id=2, name="Product 2", category="Category 2", price=20.0)
    ]
    
    # Mock the query chain: query.offset().limit().all()
    mock_offset_query = MagicMock()
    mock_limit_query = MagicMock()
    mock_query.offset.return_value = mock_offset_query
    mock_offset_query.limit.return_value = mock_limit_query
    mock_limit_query.all.return_value = mock_products
    
    result = list_products(mock_db, skip=0, limit=10, search=None)
    assert len(result) == 2
    assert result[0].name == "Product 1"
    assert result[1].name == "Product 2"
    
    # When search is provided, it should filter
    mock_filtered_query = MagicMock()
    mock_query.filter.return_value = mock_filtered_query
    mock_filtered_offset_query = MagicMock()
    mock_filtered_limit_query = MagicMock()
    mock_filtered_query.offset.return_value = mock_filtered_offset_query
    mock_filtered_offset_query.limit.return_value = mock_filtered_limit_query
    mock_filtered_limit_query.all.return_value = [mock_products[0]]
    
    result_search = list_products(mock_db, skip=0, limit=10, search="Product 1")
    assert len(result_search) == 1
    assert result_search[0].name == "Product 1"


def test_get_product():
    """Test getting a specific product"""
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_filter = MagicMock()
    mock_query.filter.return_value = mock_filter
    
    # Mock return value
    mock_product = Product(
        id=1, 
        name="Test Product", 
        category="Test Category", 
        price=10.5
    )
    mock_filter.first.return_value = mock_product
    
    result = get_product(mock_db, 1)
    
    assert result.id == 1
    assert result.name == "Test Product"
    assert result.category == "Test Category"
    assert result.price == 10.5
    
    # Test when product is not found (should return None)
    mock_filter.first.return_value = None
    result_none = get_product(mock_db, 999)
    assert result_none is None


def test_update_product():
    """Test updating a product"""
    mock_db = MagicMock()
    
    # Mock existing product
    existing_product = MagicMock()
    existing_product.id = 1
    existing_product.name = "Old Product"
    existing_product.category = "Old Category"
    existing_product.price = 5.0
    existing_product.image_path = None
    
    # Mock the get_product call to return the existing product
    with patch('app.crud.get_product', return_value=existing_product):
        result = update_product(
            mock_db, 
            1, 
            "New Product", 
            "New Category", 
            15.0, 
            "/new/image.jpg"
        )
        
        # Verify the values were updated
        assert result.name == "New Product"
        assert result.category == "New Category"
        assert result.price == 15.0
        assert result.image_path == "/new/image.jpg"
        
        # Verify database operations
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()


def test_update_product_not_found():
    """Test updating a product that doesn't exist"""
    with patch('app.crud.get_product', return_value=None):
        result = update_product(
            MagicMock(), 
            999, 
            "New Product", 
            "New Category", 
            15.0, 
            "/new/image.jpg"
        )
        
        # Should return None when product doesn't exist
        assert result is None


def test_delete_product():
    """Test deleting a product"""
    mock_db = MagicMock()
    
    # Mock existing product
    existing_product = MagicMock()
    existing_product.id = 1
    
    # Mock the get_product call to return the existing product
    with patch('app.crud.get_product', return_value=existing_product):
        delete_product(mock_db, 1)
        
        # Verify database operations
        mock_db.delete.assert_called_once_with(existing_product)
        mock_db.commit.assert_called_once()


def test_delete_product_not_found():
    """Test deleting a product that doesn't exist"""
    # Mock database session
    mock_db = MagicMock()
    # Mock the get_product call to return None
    with patch('app.crud.get_product', return_value=None):
        delete_product(mock_db, 999)
        
        # Verify that delete was not called
        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()