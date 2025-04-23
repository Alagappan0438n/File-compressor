import zlib
import os

def compress_file(input_file_path, output_file_path):
    """Compress a file using zlib compression."""
    try:
        # Open the input file in binary mode and read the content
        with open(input_file_path, 'rb') as input_file:
            file_data = input_file.read()
        
        # Compress the data using zlib
        compressed_data = zlib.compress(file_data)
        
        # Write the compressed data to the output file
        with open(output_file_path, 'wb') as output_file:
            output_file.write(compressed_data)
        
        print(f"File '{input_file_path}' successfully compressed to '{output_file_path}'")
    
    except Exception as e:
        print(f"Error during compression: {e}")

def decompress_file(input_file_path, output_file_path):
    """Decompress a zlib compressed file."""
    try:
        # Open the compressed file in binary mode and read the content
        with open(input_file_path, 'rb') as input_file:
            compressed_data = input_file.read()
        
        # Decompress the data using zlib
        decompressed_data = zlib.decompress(compressed_data)
        
        # Write the decompressed data to the output file
        with open(output_file_path, 'wb') as output_file:
            output_file.write(decompressed_data)
        
        print(f"File '{input_file_path}' successfully decompressed to '{output_file_path}'")
    
    except Exception as e:
        print(f"Error during decompression: {e}")

def get_file_size(file_path):
    """Return the size of a file in bytes."""
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        print(f"Error getting file size: {e}")
        return None

def main():
    # Example usage
    print("File Compression Tool")
    print("=====================")

    input_file = input("Enter the path of the file to compress: ").strip()
    if not os.path.isfile(input_file):
        print("The input file does not exist.")
        return
    
    compressed_file = input_file + '.zlib'
    decompress_file_path = input("Enter the path to save the decompressed file (or press Enter to skip): ").strip()

    # Compress the file
    compress_file(input_file, compressed_file)

    # Print the file sizes before and after compression
    original_size = get_file_size(input_file)
    compressed_size = get_file_size(compressed_file)

    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")

    # If a decompressed file path is given, attempt to decompress
    if decompress_file_path:
        decompress_file(compressed_file, decompress_file_path)

if _name_ == "_main_":
    main()
