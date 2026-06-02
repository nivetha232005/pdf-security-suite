import pypdf
from pypdf import PdfReader, PdfWriter
from utils.file_handler import load_file
import os

def merge_pdfs(file_ids, output_path):
    try:
        writer = PdfWriter()
        
        for file_id in file_ids:
            path = load_file(file_id)
            if path:
                reader = PdfReader(path)
                for page in reader.pages:
                    writer.add_page(page)
        
        # Save merged PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Merge error: {e}")
        return False

def split_pdf(input_path, output_path, page_range):
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        # Parse page range (e.g., "1-5" or "1,3,5")
        if '-' in page_range:
            start, end = map(int, page_range.split('-'))
            for i in range(start - 1, end):
                if i < len(reader.pages):
                    writer.add_page(reader.pages[i])
        else:
            pages = [int(p.strip()) - 1 for p in page_range.split(',')]
            for page_num in pages:
                if 0 <= page_num < len(reader.pages):
                    writer.add_page(reader.pages[page_num])
        
        # Save split PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Split error: {e}")
        return False

def rotate_pdf(input_path, output_path, rotation, pages='all'):
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        rotation_map = {90: 90, 180: 180, 270: 270}
        rotate_degrees = rotation_map.get(int(rotation), 0)
        
        if pages == 'all':
            for page in reader.pages:
                page.rotate(rotate_degrees)
                writer.add_page(page)
        else:
            page_nums = [int(p.strip()) - 1 for p in pages.split(',')]
            for i, page in enumerate(reader.pages):
                if i in page_nums:
                    page.rotate(rotate_degrees)
                writer.add_page(page)
        
        # Save rotated PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Rotate error: {e}")
        return False
