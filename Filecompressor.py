import zlib
import os

def compress_file(input_file_path, output_file_path):
    """Compress a file using zlib compression."""
    try:
        # Check if the input file exists
        if not os.path.isfile(input_file_path):
            print(f"Error: The input file '{input_file_path}' does not exist.")
            return

        # Open the input file in binary mode and read the content
        with open(input_file_path, 'rb') as input_file:
            file_data = input_file.read()
        
        # Compress the data using zlib
        compressed_data = zlib.compress(file_data)
        
        # Check if output file path is valid (directory should exist)
        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            print(f"Error: The directory '{output_dir}' does not exist.")
            return

        # Write the compressed data to the output file
        with open(output_file_path, 'wb') as output_file:
            output_file.write(compressed_data)
        
        print(f"File '{input_file_path}' successfully compressed to '{output_file_path}'")
    
    except Exception as e:
        print(f"Error during compression: {e}")

def decompress_file(input_file_path, output_file_path):
    """Decompress a zlib compressed file."""
    try:
        # Check if the compressed file exists
        if not os.path.isfile(input_file_path):
            print(f"Error: The compressed file '{input_file_path}' does not exist.")
            return

        # Open the compressed file in binary mode and read the content
        with open(input_file_path, 'rb') as input_file:
            compressed_data = input_file.read()
        
        # Attempt to decompress the data using zlib
        try:
            decompressed_data = zlib.decompress(compressed_data)
        except zlib.error as e:
            print(f"Error: Failed to decompress the file. It may be corrupt. {e}")
            return
        
        # Check if output file path is valid (directory should exist)
        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            print(f"Error: The directory '{output_dir}' does not exist.")
            return

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
    """Main function for the compression/decompression tool."""
    while True:
        print("\nFile Compression Tool")
        print("=====================")
        print("1. Compress a file")
        print("2. Decompress a file")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            # Compress a file
            input_file = input("Enter the path of the file to compress: ").strip()
            if not os.path.isfile(input_file):
                print("Error: The input file does not exist.")
                continue
            
            compressed_file = input_file + '.zlib'
            compress_file(input_file, compressed_file)

            # Print the file sizes before and after compression
            original_size = get_file_size(input_file)
            compressed_size = get_file_size(compressed_file)

            if original_size is not None and compressed_size is not None:
                print(f"Original size: {original_size} bytes")
                print(f"Compressed size: {compressed_size} bytes")
        
        elif choice == '2':
            # Decompress a file
            compressed_file = input("Enter the path of the compressed file (.zlib): ").strip()
            if not os.path.isfile(compressed_file):
                print("Error: The compressed file does not exist.")
                continue
            
            # If no decompressed file path is given, default to the same path as the zlib file
            decompress_file_path = input("Enter the path to save the decompressed file (or press Enter to use the same path as the zlib file): ").strip()

            if not decompress_file_path:
                # Remove the '.zlib' extension and use the original filename for decompression
                decompress_file_path = compressed_file.rstrip('.zlib')
            
            decompress_file(compressed_file, decompress_file_path)
            
            # Let the user know the file was decompressed and where it was saved
            print(f"Decompression successful! The decompressed file was saved as: {decompress_file_path}")

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
