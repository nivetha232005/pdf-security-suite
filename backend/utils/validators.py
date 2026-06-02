import magic

def validate_pdf(file):
    if file.filename == '':
        return False, "No file selected"
    
    if not file.filename.lower().endswith('.pdf'):
        return False, "File must be a PDF"
    
    # Check file size (max 50MB)
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    
    if size > 50 * 1024 * 1024:
        return False, "File size exceeds 50MB limit"
    
    # Check MIME type
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    
    if mime != 'application/pdf':
        return False, "Invalid file type. Only PDF files are allowed"
    
    return True, None

def validate_password(password):
    if not password:
        return False, "Password is required"
    
    if len(password) < 4:
        return False, "Password must be at least 4 characters"
    
    return True, None