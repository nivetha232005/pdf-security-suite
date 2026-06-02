from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from config import Config
import os
import uuid
from pypdf import PdfReader, PdfWriter

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=[
    'http://localhost:3000',                    # Local development
    'https://pdf-frontend-dzvm.onrender.com'    # Your production frontend
])

# Ensure directories exist
Config.ensure_directories()

# Import utilities with aliases to avoid name conflicts
from utils.validators import validate_pdf, validate_password
from utils.file_handler import save_uploaded_file, load_file, delete_file
from services.encryption_service import encrypt_pdf, decrypt_pdf
from services.pdf_service import merge_pdfs as merge_pdfs_service, split_pdf as split_pdf_service, rotate_pdf as rotate_pdf_service
from services.compression_service import compress_pdf as compress_pdf_service

@app.route('/api/upload', methods=['POST'])
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
        'size': os.path.getsize(file_path)
    })

@app.route('/api/protect', methods=['POST'])
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

@app.route('/api/remove-password', methods=['POST'])
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

@app.route('/api/merge', methods=['POST'])
def merge_pdf():
    data = request.json
    file_ids = data.get('file_ids', [])
    
    if len(file_ids) < 2:
        return jsonify({'error': 'At least 2 PDFs required for merging'}), 400
    
    output_filename = f'merged_{uuid.uuid4()}.pdf'
    output_path = os.path.join('processed', output_filename)
    
    success = merge_pdfs_service(file_ids, output_path)
    
    if success:
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{output_filename}',
            'message': 'PDFs merged successfully'
        })
    else:
        return jsonify({'error': 'Failed to merge PDFs'}), 500

@app.route('/api/split', methods=['POST'])
def split_pdf():
    data = request.json
    file_id = data.get('file_id')
    page_range = data.get('page_range')
    
    if not file_id or not page_range:
        return jsonify({'error': 'File ID and page range required'}), 400
    
    input_path = load_file(file_id)
    if not input_path:
        return jsonify({'error': 'File not found'}), 404
    
    output_filename = f'split_{uuid.uuid4()}.pdf'
    output_path = os.path.join('processed', output_filename)
    
    success = split_pdf_service(input_path, output_path, page_range)
    
    if success:
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{output_filename}',
            'message': 'PDF split successfully'
        })
    else:
        return jsonify({'error': 'Failed to split PDF'}), 500

@app.route('/api/compress', methods=['POST'])
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
    
    success, compressed_size = compress_pdf_service(input_path, output_path)
    
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

@app.route('/api/rotate', methods=['POST'])
def rotate_pdf():
    data = request.json
    file_id = data.get('file_id')
    rotation = data.get('rotation')
    pages = data.get('pages', 'all')
    
    if not file_id or not rotation:
        return jsonify({'error': 'File ID and rotation angle required'}), 400
    
    input_path = load_file(file_id)
    if not input_path:
        return jsonify({'error': 'File not found'}), 404
    
    output_filename = f'rotated_{uuid.uuid4()}.pdf'
    output_path = os.path.join('processed', output_filename)
    
    success = rotate_pdf_service(input_path, output_path, rotation, pages)
    
    if success:
        return jsonify({
            'success': True,
            'download_url': f'/api/download/{output_filename}',
            'message': f'PDF rotated {rotation}° successfully'
        })
    else:
        return jsonify({'error': 'Failed to rotate PDF'}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    file_path = os.path.join('processed', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    # Use PORT environment variable from Render, default to 5000 for local
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production
