import pikepdf

def encrypt_pdf(input_path, output_path, password):
    try:
        with pikepdf.open(input_path) as pdf:
            pdf.save(output_path, encryption=pikepdf.Encryption(
                user=password,
                owner=password,
                allow=pikepdf.Permissions(print=True, extract=True)
            ))
        return True
    except Exception as e:
        print(f"Encryption error: {e}")
        return False

def decrypt_pdf(input_path, output_path, password):
    try:
        with pikepdf.open(input_path, password=password) as pdf:
            pdf.save(output_path)
        return True
    except Exception as e:
        print(f"Decryption error: {e}")
        return False