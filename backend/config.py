import os
from datetime import datetime

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    UPLOAD_FOLDER = 'uploads'
    PROCESSED_FOLDER = 'processed'
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Cleanup old files after 1 hour
    CLEANUP_INTERVAL = 3600
    
    @staticmethod
    def ensure_directories():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.PROCESSED_FOLDER, exist_ok=True)
