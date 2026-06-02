import pikepdf
import os

def compress_pdf(input_path, output_path):
    """
    Compress PDF file by optimizing images and streams
    """
    try:
        # Open the PDF
        with pikepdf.Pdf.open(input_path) as pdf:
            # Save with compression options
            pdf.save(output_path, 
                    compress_streams=True,
                    stream_decode_level=pikepdf.StreamDecodeLevel.specialized)
        
        # Get compressed size
        compressed_size = os.path.getsize(output_path)
        
        # If compression didn't reduce size, use original
        original_size = os.path.getsize(input_path)
        if compressed_size >= original_size:
            # Copy original file instead
            import shutil
            shutil.copy2(input_path, output_path)
            compressed_size = original_size
        
        return True, compressed_size
        
    except Exception as e:
        print(f"Compression error details: {e}")
        return False, 0