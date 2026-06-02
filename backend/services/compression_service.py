import pypdf
from pypdf import PdfReader, PdfWriter
import os

def compress_pdf(input_path, output_path):
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        original_size = os.path.getsize(input_path)
        
        # Copy all pages with compression
        for page in reader.pages:
            writer.add_page(page)
        
        # Compress by enabling compression
        writer.compress_content_streams = True
        
        # Save compressed PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        compressed_size = os.path.getsize(output_path)
        
        # If compression didn't help, use original
        if compressed_size >= original_size:
            import shutil
            shutil.copy2(input_path, output_path)
            compressed_size = original_size
        
        return True, compressed_size
        
    except Exception as e:
        print(f"Compression error: {e}")
        return False, 0
