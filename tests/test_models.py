import pytest
from app.models import Product, User
from sqlalchemy import Column, Integer, String, Float, Boolean


def test_product_model_structure():
    """Test the structure of the Product model"""
    # Check the table name
    assert Product.__tablename__ == "product"
    
    # Check that the columns exist with correct types
    assert hasattr(Product, 'id')
    assert hasattr(Product, 'name')
    assert hasattr(Product, 'category')
    assert hasattr(Product, 'price')
    assert hasattr(Product, 'image_path')
    
    # Check column types
    assert isinstance(Product.id.property.columns[0].type, Integer)
    assert isinstance(Product.name.property.columns[0].type, String)
    assert isinstance(Product.category.property.columns[0].type, String)
    assert isinstance(Product.price.property.columns[0].type, Float)
    assert isinstance(Product.image_path.property.columns[0].type, String)


def test_user_model_structure():
    """Test the structure of the User model"""
    # Check the table name
    assert User.__tablename__ == "users"
    
    # Check that the columns exist with correct types
    assert hasattr(User, 'id')
    assert hasattr(User, 'username')
    assert hasattr(User, 'hashed_password')
    assert hasattr(User, 'is_admin')
    
    # Check column types
    assert isinstance(User.id.property.columns[0].type, Integer)
    assert isinstance(User.username.property.columns[0].type, String)
    assert isinstance(User.hashed_password.property.columns[0].type, String)
    assert isinstance(User.is_admin.property.columns[0].type, Boolean)


def test_product_model_nullable():
    """Test that Product model has correct nullable settings"""
    # Check nullable settings
    for column in Product.__table__.columns:
        if column.name == 'name':
            assert column.nullable == False
        elif column.name == 'category':
            assert column.nullable == False
        elif column.name == 'price':
            assert column.nullable == False
        elif column.name == 'image_path':
            assert column.nullable == True
        elif column.name == 'id':
            assert column.nullable == False  # Primary key