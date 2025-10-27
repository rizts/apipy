import pytest
from pydantic import ValidationError
from app.schemas import ProductBase, ProductCreate, ProductUpdate, ProductResponse, UserCreate, UserLogin, Token


def test_product_base_schema():
    """Test the ProductBase schema"""
    # Valid data
    data = {
        "name": "Test Product",
        "category": "Test Category",
        "price": 10.5
    }
    product_base = ProductBase(**data)
    
    assert product_base.name == "Test Product"
    assert product_base.category == "Test Category"
    assert product_base.price == 10.5


def test_product_create_schema():
    """Test the ProductCreate schema"""
    # Valid data
    data = {
        "name": "Test Product",
        "category": "Test Category",
        "price": 10.5
    }
    product_create = ProductCreate(**data)
    
    assert product_create.name == "Test Product"
    assert product_create.category == "Test Category"
    assert product_create.price == 10.5


def test_product_update_schema():
    """Test the ProductUpdate schema"""
    # Valid data
    data = {
        "name": "Updated Product",
        "category": "Updated Category",
        "price": 15.75
    }
    product_update = ProductUpdate(**data)
    
    assert product_update.name == "Updated Product"
    assert product_update.category == "Updated Category"
    assert product_update.price == 15.75


def test_product_response_schema():
    """Test the ProductResponse schema"""
    # Valid data with id
    data = {
        "id": 1,
        "name": "Test Product",
        "category": "Test Category", 
        "price": 10.5,
        "image_path": "/path/to/image.jpg"
    }
    product_response = ProductResponse(**data)
    
    assert product_response.id == 1
    assert product_response.name == "Test Product"
    assert product_response.category == "Test Category"
    assert product_response.price == 10.5
    assert product_response.image_path == "/path/to/image.jpg"
    
    # Test with optional image_path as None
    data_optional = {
        "id": 2,
        "name": "Test Product 2",
        "category": "Test Category 2",
        "price": 20.0,
        "image_path": None
    }
    product_response_optional = ProductResponse(**data_optional)
    
    assert product_response_optional.id == 2
    assert product_response_optional.image_path is None


def test_product_response_schema_validation():
    """Test validation for ProductResponse schema"""
    # Missing required field should raise ValidationError
    with pytest.raises(ValidationError):
        ProductResponse(
            name="Test Product",
            category="Test Category",
            price=10.5
        )


def test_user_create_schema():
    """Test the UserCreate schema"""
    # Valid data
    data = {
        "username": "testuser",
        "password": "testpassword",
        "is_admin": False
    }
    user_create = UserCreate(**data)
    
    assert user_create.username == "testuser"
    assert user_create.password == "testpassword"
    assert user_create.is_admin == False


def test_user_login_schema():
    """Test the UserLogin schema"""
    # Valid data
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    user_login = UserLogin(**data)
    
    assert user_login.username == "testuser"
    assert user_login.password == "testpassword"


def test_token_schema():
    """Test the Token schema"""
    # Valid data
    data = {
        "access_token": "test_token_value",
        "token_type": "bearer"
    }
    token = Token(**data)
    
    assert token.access_token == "test_token_value"
    assert token.token_type == "bearer"