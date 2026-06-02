from flask import Blueprint, request, jsonify
from services.compression_service import compress_pdf
from utils.file_handler import load_file
import os
import uuid

compress_bp = Blueprint('compress', __name__)

@compress_bp.route('/api/compress', methods=['POST'])
def compress_pdf():
    data = request.json
    file_id = data.get('file_id')
    
    if not file_id:
        return jsonify({'error': 'File ID required'}), 400
    
    input_path = load_file(file_id)
    if not input_path:
        return jsonify({'error': 'File not found'}), 404
    
    original_size = os.path.getsize(input_path)
    
    output_filename = f'compressed_{uuid.uuid4()}.pdf'
    output_path = os.path.join('processed', output_filename)
    
    success, compressed_size = compress_pdf(input_path, output_path)
    
    if success:
        reduction = ((original_size - compressed_size) / original_size) * 100
        return jsonify({
            'success': True,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'reduction': round(reduction, 2),
            'download_url': f'/api/download/{output_filename}',
            'message': 'PDF compressed successfully'
        })
    else:
        return jsonify({'error': 'Failed to compress PDF'}), 500