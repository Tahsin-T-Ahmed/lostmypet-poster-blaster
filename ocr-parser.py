import os
from PIL import Image
import pytesseract

def get_file_path(prompt_msg: str="Enter file path") -> str:

    msg = f"{prompt_msg}: " # Format prompt message

    # Prompt user for file path, remove quotes if any
    path = input(msg).replace('"', '').replace("'", '')

    # Validate file path
    while not os.path.isfile(path):
        print("Invalid file path. Please try again.")
        path = input(msg).replace('"', '').replace("'", '')

    path = os.path.abspath(path) # Convert to absolute path

    return path

if "__main__" == __name__:
    img_file_path = get_file_path("Enter the image file path")
    print(img_file_path)