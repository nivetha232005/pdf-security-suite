import pypdf
from pypdf import PdfReader, PdfWriter
import os

def encrypt_pdf(input_path, output_path, password):
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)
        
        # Add password encryption
        writer.encrypt(password)
        
        # Save encrypted PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Encryption error: {e}")
        return False

def decrypt_pdf(input_path, output_path, password):
    try:
        reader = PdfReader(input_path)
        
        # Check if PDF is encrypted
        if reader.is_encrypted:
            reader.decrypt(password)
        
        writer = PdfWriter()
        
        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)
        
        # Save decrypted PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Decryption error: {e}")
        return False
