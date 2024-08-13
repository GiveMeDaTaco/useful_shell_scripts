import os
import base64
import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image

# Step 1: Encode each file to Base64
def encode_file_to_base64(file_path):
    with open(file_path, "rb") as f:
        encoded_data = base64.b64encode(f.read())
    return encoded_data

# Step 2: Generate QR code for the encoded file data
def generate_qr_code(file_data, output_file):
    qr = pyqrcode.create(file_data.decode('utf-8'), error='M', version=20)
    qr.png(output_file, scale=8)

# Step 3: Walk through the directory, encode each file, and generate QR codes
def process_directory(input_directory, qr_output_dir):
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            file_path = os.path.join(root, file)
            encoded_data = encode_file_to_base64(file_path)
            
            # Create corresponding directory structure in output directory
            relative_path = os.path.relpath(root, input_directory)
            qr_file_dir = os.path.join(qr_output_dir, relative_path)
            if not os.path.exists(qr_file_dir):
                os.makedirs(qr_file_dir)
            
            # Generate QR code for the file
            qr_file_path = os.path.join(qr_file_dir, f"{file}.png")
            generate_qr_code(encoded_data, qr_file_path)
            print(f"Generated QR code for {file_path} -> {qr_file_path}")

# Step 4: Decode QR codes and reconstruct files
def decode_qr_codes(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".png"):
                qr_code_path = os.path.join(root, file)
                qr = Image.open(qr_code_path)
                decoded_data = decode(qr)[0].data
                
                # Decode Base64 and write back to file
                relative_path = os.path.relpath(root, input_dir)
                output_file_dir = os.path.join(output_dir, relative_path)
                if not os.path.exists(output_file_dir):
                    os.makedirs(output_file_dir)
                
                original_file_name = os.path.splitext(file)[0]
                output_file_path = os.path.join(output_file_dir, original_file_name)
                with open(output_file_path, "wb") as f:
                    f.write(base64.b64decode(decoded_data))
                print(f"Reconstructed file {output_file_path}")

# Main function to execute the steps
def main(input_directory, qr_output_dir, reconstructed_dir):
    # Process the directory and generate QR codes for each file
    process_directory(input_directory, qr_output_dir)
    
    print(f"QR codes generated in directory: {qr_output_dir}")
    
    # Decode QR codes and reconstruct the original files
    decode_qr_codes(qr_output_dir, reconstructed_dir)
    
    print(f"Files reconstructed in directory: {reconstructed_dir}")

# Example usage
if __name__ == "__main__":
    input_directory = "input_directory"  # Replace with your directory path
    qr_output_dir = "qr_codes"
    reconstructed_dir = "reconstructed_files"
    
    main(input_directory, qr_output_dir, reconstructed_dir)
