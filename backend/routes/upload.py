from flask import Blueprint, request, jsonify
from utils.validators import validate_pdf
from utils.file_handler import save_uploaded_file
import uuid

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    is_valid, error = validate_pdf(file)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    file_id = str(uuid.uuid4())
    file_path = save_uploaded_file(file, file_id)
    
    return jsonify({
        'success': True,
        'file_id': file_id,
        'filename': file.filename,
        'size': file.content_length
    })