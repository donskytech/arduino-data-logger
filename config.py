#!/usr/bin/env python

import os 
from dotenv import load_dotenv
load_dotenv()

# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class
    """
    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='f04be22ca32b6dbe3b2599fc10b9f673') # generated using secrets.token_hex(16)
    
    MONGO_DB_USERNAME = os.getenv("MONGODB_USERNAME")
    MONGO_DB_PASSWORD = os.getenv("MONGODB_PASSWORD")
    MONGO_DB_HOST = os.getenv("MONGODB_HOST")
    MONGODB_DB = os.getenv("MONGODB_DB")
    db_url = f"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}/{MONGODB_DB}?retryWrites=true&w=majority"
    MONGO_URI= db_url
    
class DevelopmentConfig(Config):
    DEBUG = True