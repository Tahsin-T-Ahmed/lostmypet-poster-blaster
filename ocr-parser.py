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

def get_raw_image(img_path: str) -> Image.Image:

    img = Image.open(img_path) # Open image file

    # Make sure image has standard dimensions as seen in the emails
    img = img.resize((813, 1053))

    return img

def get_image_segments(img: Image.Image) -> dict[str, Image.Image]:

    img_segments = dict()

    # crop image into segments based on predefined coordinates

    return img_segments

if "__main__" == __name__:
    poster_file_path = get_file_path("Enter the image file path")
    
    poster_raw = get_raw_image(poster_file_path)
    poster_raw.show()