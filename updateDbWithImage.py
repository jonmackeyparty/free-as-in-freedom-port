import os
import re
import click
import vertexai
import asyncio
from cv2 import cv2
from tinydb import TinyDB
from dotenv import load_dotenv
from image_creator.stable_diffusion_openvino.makeImage import makeImage, reduceTool
from PIL import Image, ImageEnhance, ImageFilter
from vertexai.preview.vision_models import ImageGenerationModel
from utils.parseUtils import create_dict, _parse_line, check_dup


def create_vertex_image(prompt, output_file):
    load_dotenv()
    vertexai.init()
    model = ImageGenerationModel.from_pretrained("imagegeneration@002")
    print(f"Generating image for: {prompt}")

    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        language="en",
        aspect_ratio="1:1",   
    )

    images[0].save(location=output_file, include_generation_parameters=False)


def addItemsToDb():
    load_dotenv()
    filepath = os.getenv('TXTFILEPATH')
    db = TinyDB(os.getenv('DBFILEPATH'))
    db2 = TinyDB(os.getenv('DB2FILEPATH'))
    img_file_path = os.getenv('IMGFILEPATH')
    data = create_dict(filepath)
    for key, value in data.items():
        if not check_dup(db, key) and not check_dup(db2, key):
            print(f"Found new record, inserting {key}")
            output_file = re.sub('[^A-Za-z0-9]+', '', key)
            write_path = f"{img_file_path}{output_file}.png"
            choice = False
            while choice is False:
                create_vertex_image(f"{key}, cellphone photograph", write_path)
                reduceTool(write_path)
                im = Image.open(write_path)
                im.show()
                choice = click.confirm('Do you want to keep the displayed image?', default =True) 
            print(f"SUCCESS: SAVED {key} to: {write_path}.")
            db.insert({'title': key, 'body': value})
                  
if __name__=="__main__":
    addItemsToDb()
