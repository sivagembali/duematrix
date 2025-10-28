import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # PostgreSQL Database Configuration
    POSTGRES_USER = os.environ.get('POSTGRES_USER') or 'postgres'
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD') or 'password'
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST') or 'localhost'
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT') or '5432'
    POSTGRES_DB = os.environ.get('POSTGRES_DB') or 'credit_bill_tracker'
    
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
        f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}