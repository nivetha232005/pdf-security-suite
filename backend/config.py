import os
import secrets
from pathlib import Path

# Get the absolute path to the backend directory
BACKEND_DIR = Path(__file__).parent.absolute()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    
    # Use absolute paths
    UPLOAD_FOLDER = str(BACKEND_DIR / 'uploads')
    PROCESSED_FOLDER = str(BACKEND_DIR / 'processed')
    ALLOWED_EXTENSIONS = {'pdf'}
    CLEANUP_INTERVAL = 3600
    
    @staticmethod
    def ensure_directories():
        """Create necessary directories if they don't exist"""
        try:
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            os.makedirs(Config.PROCESSED_FOLDER, exist_ok=True)
        except FileExistsError:
            # Directory already exists, that's fine
            pass
        except Exception as e:
            print(f"Warning: Could not create directory: {e}")
