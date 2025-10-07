import os
from PIL import Image
import pytesseract
import calendar
import json

def get_months() -> dict[str, str]:
    return list(calendar.month_name)

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

def extract_image_text(img: Image.Image) -> str:
    """
    Extract text from the input image using OCR and return it as a string.
    """

    extracted_text = pytesseract.image_to_string(img)

    return extracted_text

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

    segments["sex"] = img.crop((540, 590, right, 635)) # crop sex (e.g.: "F")

    segments["color"] = img.crop((170, 625, right, 675)) # crop color (e.g.: "Black")
    
    segments["bottom_details"] = img.crop((200, 670, right, img.size[1])) # crop remaining details at the end of poster

    return segments

def img_crops_to_json(segments: dict[str, Image.Image]) -> dict[str, str]:
    """
    Read text from each image segment and return them as a dictionary.
    """

    poster_info = dict()

    for key, cropped_img in segments.items():

        if "bottom_details" == key:
            # For bottom details, extract multiple lines of text
            bottom_details = extract_image_text(cropped_img).split("\n\n")

            bottom_details.pop(2) # Remove "You Have Any Information Please Contact:"

            # GET "DETAILS" FIELD FROM POSTER
            
            details = bottom_details[0].replace('\n', ' ').strip() # Get first list item

            details = " ... ".join(details.split("...")) # Add spaces around ellipses

            poster_info["details"] = details    # Set JSON object's "details" as cleaned value 

            
            
            # GET "LAST SEEN" FIELD FROM POSTER

            last_seen = bottom_details[1][3:].strip().replace('\n', ' ') # Remove "an:" and clean whitespace
            
            poster_info["last_seen"] = last_seen # Set JSON object's "last_seen" as cleaned  value

            # GET "CONTACT" FIELD FROM POSTER

            contact = bottom_details[2].strip()[:12]

            poster_info["contact"] = contact # Set JSON object's "contact" as cleaned value

            # GET "EMAIL" AND "PET ID" FIELDS FROM POSTER

            email, pet_id = bottom_details[3].strip().split(' ')

            poster_info["email"] = email.strip() # Set JSON object's "email" as cleaned value
            poster_info["pet_id"] = pet_id.strip() # Set JSON object's "pet_id" as cleaned value

            continue # End of "bottom_details" processing

        if "sex" == key:
            sex = extract_image_text(cropped_img).strip()

            sex = sex.split(' ')[1] # Get second term after space (e.g.: "M")

            poster_info["sex"] = sex.strip() # Set JSON object's "sex" value as cleaned value

            continue # End of "sex" processing

        if "info" == key:
            info = extract_image_text(cropped_img).strip()
            date = info[-8:].strip() # Get last 8 characters (e.g.: "09/27/25")
            name = info[:-13].strip()

            # Remove quotation marks from name
            name = name.replace("'", '')
            name = name.replace('"', '')

            # Change date month to three-letter abbreviation, to avoid international format confusion
            month_index = int(date[:2])
            month = get_months()[month_index]
            month_abbr = month[:3].upper()
            date = month_abbr + date[2:]

            # Set "name" and "date" variables to newly cleaned values in poster_info dictionary
            poster_info["name"], poster_info["date"] = name, date

            continue # End of "info" processing

        poster_info[key] = extract_image_text(cropped_img).strip() # Set other fields as extracted values


    # CONVERT TO JSON AND RETURN
    poster_json = json.dumps(poster_info)
    return poster_json


if "__main__" == __name__:
    poster_file_path = get_file_path("Enter the image file path")
    
    poster_raw = get_raw_image(poster_file_path)

    poster_crops = get_image_segments(poster_raw)

    poster_contents = img_crops_to_json(poster_crops)
    print("Poster contents:\n", poster_contents)