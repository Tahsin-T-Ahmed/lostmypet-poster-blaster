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
    """
    Crop the input image into predefined segments and return them as a dictionary.
    """

    left, right = 67, 745
    top = 23

    segments = dict()

    segments["website"] = img.crop((left, top, right, 110)) # crop website (e.g.: LostMyDoggie.com)

    segments["headline"] = img.crop((left, 100, right, 190)) # crop headline (e.g.: "LOST DOG")

    segments["info"] = img.crop((left, 180, right, 232)) # crop info (e.g.: "PetName" Lost 09/27/25)

    segments["breed"] = img.crop((184, 590, 548, 635)) # crop breed (e.g.: "German Shepherd")

    segments["sex"] = img.crop((625, 590, right, 635)) # crop sex (e.g.: "F")

    segments["color"] = img.crop((170, 625, right, 675)) # crop color (e.g.: "Black")

       

    return segments

if "__main__" == __name__:
    poster_file_path = get_file_path("Enter the image file path")
    
    poster_raw = get_raw_image(poster_file_path)

    poster_crops = get_image_segments(poster_raw)
    poster_key = "color"
    poster_crops[poster_key].show()