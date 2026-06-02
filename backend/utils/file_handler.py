import os
import shutil
from config import Config
import uuid

def save_uploaded_file(file, file_id):
    filename = f"{file_id}.pdf"
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath

def load_file(file_id):
    filepath = os.path.join(Config.UPLOAD_FOLDER, f"{file_id}.pdf")
    if os.path.exists(filepath):
        return filepath
    return None

def delete_file(filepath):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def cleanup_old_files():
    import time
    current_time = time.time()
    
    for folder in [Config.UPLOAD_FOLDER, Config.PROCESSED_FOLDER]:
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.getmtime(filepath) < current_time - Config.CLEANUP_INTERVAL:
                os.remove(filepath)