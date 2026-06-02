import pikepdf
from utils.file_handler import load_file
import os

def merge_pdfs(file_ids, output_path):
    try:
        pdfs = []
        for file_id in file_ids:
            path = load_file(file_id)
            if path:
                pdfs.append(pikepdf.Pdf.open(path))
        
        if not pdfs:
            return False
        
        output_pdf = pikepdf.Pdf.new()
        for pdf in pdfs:
            output_pdf.pages.extend(pdf.pages)
        
        output_pdf.save(output_path)
        
        # Clean up
        for pdf in pdfs:
            pdf.close()
        
        return True
    except Exception as e:
        print(f"Merge error: {e}")
        return False

def split_pdf(input_path, output_path, page_range):
    try:
        with pikepdf.Pdf.open(input_path) as pdf:
            output_pdf = pikepdf.Pdf.new()
            
            # Parse page range (e.g., "1-5" or "1,3,5")
            if '-' in page_range:
                start, end = map(int, page_range.split('-'))
                for i in range(start - 1, end):
                    if i < len(pdf.pages):
                        output_pdf.pages.append(pdf.pages[i])
            else:
                pages = [int(p.strip()) - 1 for p in page_range.split(',')]
                for page_num in pages:
                    if 0 <= page_num < len(pdf.pages):
                        output_pdf.pages.append(pdf.pages[page_num])
            
            output_pdf.save(output_path)
        return True
    except Exception as e:
        print(f"Split error: {e}")
        return False

def rotate_pdf(input_path, output_path, rotation, pages='all'):
    try:
        with pikepdf.Pdf.open(input_path) as pdf:
            rotation_angle = int(rotation)
            
            if pages == 'all':
                for page in pdf.pages:
                    page.Rotate = (page.get('/Rotate', 0) + rotation_angle) % 360
            else:
                # Rotate specific pages (1-indexed)
                page_nums = [int(p.strip()) - 1 for p in pages.split(',')]
                for i, page in enumerate(pdf.pages):
                    if i in page_nums:
                        page.Rotate = (page.get('/Rotate', 0) + rotation_angle) % 360
            
            pdf.save(output_path)
        return True
    except Exception as e:
        print(f"Rotate error: {e}")
        return False