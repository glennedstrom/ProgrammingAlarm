# config.py
import os
from pathlib import Path

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    
    # Application paths
    BASE_DIR = Path(__file__).parent
    PROBLEMS_DIR = BASE_DIR / 'app' / 'problems'
    STATIC_DIR = BASE_DIR / 'app' / 'static'
    
    # Ensure required directories exist
    PROBLEMS_DIR.mkdir(exist_ok=True)
    (STATIC_DIR / 'sounds').mkdir(exist_ok=True, parents=True)
    
    # Security settings
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600  # 1 hour
    
    # Custom settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'py', 'md', 'yaml', 'mp3'}

