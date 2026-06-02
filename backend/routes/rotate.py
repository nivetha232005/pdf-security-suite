from flask import Blueprint, request, jsonify
from services.pdf_service import rotate_pdf
from utils.file_handler import load_file
import os
import uuid

rotate_bp = Blueprint('rotate', __name__)

@rotate_bp.route('/api/rotate', methods=['POST'])
def rotate_pdf():
    data = request.json
    file_id = data.get('file_id')
    rotation = data.get('rotation')  # 90, 180, 270
    pages = data.get('pages', 'all')  # 'all' or list of page numbers
    
    if not file_id or not rotation:
        return jsonify({'error': 'File ID and rotation angle required'}), 400
    
    input_path = load_file(file_id)
    if not input_path:
        return jsonify({'error': 'File not found'}), 404
    
    output_filename = f'rotated_{uuid.uuid4()}.pdf'
    output_path = os.path.join('processed', output_filename)
    
    success = rotate_pdf(input_path, output_path, rotation, pages)
    
    if success:
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{output_filename}',
            'message': f'PDF rotated {rotation}° successfully'
        })
    else:
        return jsonify({'error': 'Failed to rotate PDF'}), 500