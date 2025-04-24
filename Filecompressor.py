import zlib
import os
from tkinter import Tk, filedialog

def compress_file(input_file_path, output_file_path):
    """Compress a file using zlib compression."""
    try:
        if not os.path.isfile(input_file_path):
            print(f"Error: The input file '{input_file_path}' does not exist.")
            return

        with open(input_file_path, 'rb') as input_file:
            file_data = input_file.read()

        compressed_data = zlib.compress(file_data)

        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            print(f"Error: The directory '{output_dir}' does not exist.")
            return

        with open(output_file_path, 'wb') as output_file:
            output_file.write(compressed_data)

        print(f"File '{input_file_path}' successfully compressed to '{output_file_path}'")

    except Exception as e:
        print(f"Error during compression: {e}")

def decompress_file(input_file_path, output_file_path):
    """Decompress a zlib compressed file."""
    try:
        if not os.path.isfile(input_file_path):
            print(f"Error: The compressed file '{input_file_path}' does not exist.")
            return

        with open(input_file_path, 'rb') as input_file:
            compressed_data = input_file.read()

        try:
            decompressed_data = zlib.decompress(compressed_data)
        except zlib.error as e:
            print(f"Error: Failed to decompress the file. It may be corrupt. {e}")
            return

        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            print(f"Error: The directory '{output_dir}' does not exist.")
            return

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

        root = Tk()
        root.withdraw()  # Hide the root window

        if choice == '1':
            input_file = filedialog.askopenfilename(title="Select File to Compress")
            if not input_file:
                print("No file selected.")
                continue

            save_path = filedialog.asksaveasfilename(
                title="Save Compressed File As",
                defaultextension=".zlib",
                filetypes=[("Zlib Compressed Files", "*.zlib")]
            )

            if not save_path:
                print("No save location selected.")
                continue

            compress_file(input_file, save_path)

            original_size = get_file_size(input_file)
            compressed_size = get_file_size(save_path)

            if original_size is not None and compressed_size is not None:
                print(f"Original size: {original_size} bytes")
                print(f"Compressed size: {compressed_size} bytes")

        elif choice == '2':
            compressed_file = filedialog.askopenfilename(
                title="Select Compressed (.zlib) File",
                filetypes=[("Zlib Compressed Files", "*.zlib")]
            )

            if not compressed_file:
                print("No file selected.")
                continue

            save_path = filedialog.asksaveasfilename(
                title="Save Decompressed File As"
            )

            if not save_path:
                print("No save location selected.")
                continue

            decompress_file(compressed_file, save_path)
            print(f"Decompression successful! The decompressed file was saved as: {save_path}")

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
