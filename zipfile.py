import os
import base64
import zipfile
import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image

# Step 1: Compress the directory
def compress_directory(input_directory, output_zipfile):
    with zipfile.ZipFile(output_zipfile, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(input_directory):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                           os.path.join(input_directory, '..')))

# Step 2: Encode the ZIP file into Base64
def encode_zip_to_base64(zipfile_path):
    with open(zipfile_path, "rb") as f:
        encoded_data = base64.b64encode(f.read())
    return encoded_data

# Step 3: Split Base64 string into chunks
def split_base64_string(encoded_data, chunk_size=5000):
    return [encoded_data[i:i + chunk_size] for i in range(0, len(encoded_data), chunk_size)]

# Step 4: Generate QR codes for each chunk
def generate_qr_codes(chunks, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, chunk in enumerate(chunks):
        qr = pyqrcode.create(chunk.decode('utf-8'), error='M', version=20)
        qr.png(os.path.join(output_dir, f'qrcode_{i + 1}.png'), scale=8)

# Step 5: Decode QR codes and reassemble the data
def decode_qr_codes(input_dir):
    decoded_chunks = []
    for qr_code_file in sorted(os.listdir(input_dir)):
        if qr_code_file.endswith(".png"):
            qr = Image.open(os.path.join(input_dir, qr_code_file))
            qr_data = decode(qr)[0].data
            decoded_chunks.append(qr_data)
    
    decoded_data = b''.join(decoded_chunks)
    return decoded_data

# Step 6: Decode Base64 and unzip the data
def decode_base64_to_zip(decoded_data, output_zipfile):
    with open(output_zipfile, "wb") as f:
        f.write(base64.b64decode(decoded_data))
    with zipfile.ZipFile(output_zipfile, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(output_zipfile))

# Main function to execute the steps
def main(input_directory, qr_output_dir, reconstructed_zip):
    compressed_file = 'compressed_directory.zip'
    
    # Compress the directory
    compress_directory(input_directory, compressed_file)
    
    # Encode the ZIP file to Base64
    encoded_data = encode_zip_to_base64(compressed_file)
    
    # Split the encoded data into chunks
    chunks = split_base64_string(encoded_data)
    
    # Generate QR codes for each chunk
    generate_qr_codes(chunks, qr_output_dir)
    
    print(f"QR codes generated in directory: {qr_output_dir}")
    
    # Decode QR codes and reassemble the data
    reassembled_data = decode_qr_codes(qr_output_dir)
    
    # Decode the Base64 back to ZIP and extract it
    decode_base64_to_zip(reassembled_data, reconstructed_zip)
    
    print(f"Data reassembled and extracted to: {reconstructed_zip}")

# Example usage
if __name__ == "__main__":
    input_directory = "input_directory"  # Replace with your directory path
    qr_output_dir = "qr_codes"
    reconstructed_zip = "reconstructed_directory.zip"
    
    main(input_directory, qr_output_dir, reconstructed_zip)
