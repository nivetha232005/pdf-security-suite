from flask import Blueprint, request, jsonify
from services.pdf_service import merge_pdfs
import os
import uuid

merge_bp = Blueprint('merge', __name__)

@merge_bp.route('/api/merge', methods=['POST'])
def merge_pdf():
    data = request.json
    file_ids = data.get('file_ids', [])
    
    if len(file_ids) < 2:
        return jsonify({'error': 'At least 2 PDFs required for merging'}), 400
    
    output_filename = f'merged_{uuid.uuid4()}.pdf'
    output_path = os.path.join('processed', output_filename)
    
    success = merge_pdfs(file_ids, output_path)
    
    if success:
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{output_filename}',
            'message': 'PDFs merged successfully'
        })
    else:
        return jsonify({'error': 'Failed to merge PDFs'}), 500