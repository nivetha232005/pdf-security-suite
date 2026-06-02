from flask import Blueprint, request, jsonify
from services.pdf_service import split_pdf
from utils.file_handler import load_file
import os
import uuid

split_bp = Blueprint('split', __name__)

@split_bp.route('/api/split', methods=['POST'])
def split_pdf():
    data = request.json
    file_id = data.get('file_id')
    page_range = data.get('page_range')  # e.g., "1-5" or "1,3,5"
    
    if not file_id or not page_range:
        return jsonify({'error': 'File ID and page range required'}), 400
    
    input_path = load_file(file_id)
    if not input_path:
        return jsonify({'error': 'File not found'}), 404
    
    output_filename = f'split_{uuid.uuid4()}.pdf'
    output_path = os.path.join('processed', output_filename)
    
    success = split_pdf(input_path, output_path, page_range)
    
    if success:
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{output_filename}',
            'message': 'PDF split successfully'
        })
    else:
        return jsonify({'error': 'Failed to split PDF'}), 500