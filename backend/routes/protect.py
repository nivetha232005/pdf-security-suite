from flask import Blueprint, request, jsonify
from services.encryption_service import encrypt_pdf
from utils.validators import validate_password
from utils.file_handler import load_file, delete_file
import os

protect_bp = Blueprint('protect', __name__)

@protect_bp.route('/api/protect', methods=['POST'])
def protect_pdf():
    data = request.json
    file_id = data.get('file_id')
    password = data.get('password')
    
    if not file_id or not password:
        return jsonify({'error': 'File ID and password required'}), 400
    
    is_valid, error = validate_password(password)
    if not is_valid:
        return jsonify({'error': error}), 400
    
    input_path = load_file(file_id)
    if not input_path:
        return jsonify({'error': 'File not found'}), 404
    
    output_filename = f'protected_{file_id}.pdf'
    output_path = os.path.join('processed', output_filename)
    
    success = encrypt_pdf(input_path, output_path, password)
    
    if success:
        delete_file(input_path)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{output_filename}',
            'message': 'PDF protected successfully'
        })
    else:
        return jsonify({'error': 'Failed to protect PDF'}), 500