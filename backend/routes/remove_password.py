from flask import Blueprint, request, jsonify
from services.encryption_service import decrypt_pdf
from utils.file_handler import load_file, delete_file
import os

remove_password_bp = Blueprint('remove_password', __name__)

@remove_password_bp.route('/api/remove-password', methods=['POST'])
def remove_password():
    data = request.json
    file_id = data.get('file_id')
    password = data.get('password')
    
    if not file_id or not password:
        return jsonify({'error': 'File ID and password required'}), 400
    
    input_path = load_file(file_id)
    if not input_path:
        return jsonify({'error': 'File not found'}), 404
    
    output_filename = f'unlocked_{file_id}.pdf'
    output_path = os.path.join('processed', output_filename)
    
    success = decrypt_pdf(input_path, output_path, password)
    
    if success:
        delete_file(input_path)
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{output_filename}',
            'message': 'Password removed successfully'
        })
    else:
        return jsonify({'error': 'Incorrect password or corrupted file'}), 401