import os
import re
import click
import vertexai
from tinydb import TinyDB
from dotenv import load_dotenv
from PIL import Image
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.generative_models import GenerativeModel
from image_creator.stable_diffusion_openvino.makeImage import reduceTool
from utils.parseUtils import create_dict, check_dup, remove_child_terms


def create_vertex_image(prompt, output_file):
    """Sends prompt to Vertex AI to generate an image, saves to write path"""
    vertexai.init()
    model = ImageGenerationModel.from_pretrained("imagegeneration@002")
    print(f"Generating image for: {prompt}")
    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        language="en",
        aspect_ratio="1:1"
    )
    images[0].save(location=output_file, include_generation_parameters=False)

def create_vertex_prompt(title, body):
    """Creates a prompt for Vertex AI from title and body"""
    vertexai.init()
    model = GenerativeModel("gemini-1.5-flash-002")
    response = model.generate_content("The following is a title and description for an item in a craiglist post.  Respond with a succinct prompt that will enable google vertex to generate an image for it. Alter any terms that would trigger google safety settings. The title is: " + title + " and the description is: " + body + ". The image should be a cellphone photograph and a rough photo typical of a self-posted ad on craiglist. Respond with the prompt only")
    prompt = response.text
    return prompt

def add_items_to_db():
    """Updates Active Db with new items from txt file"""
    load_dotenv()
    filepath = os.getenv('TXTFILEPATH')
    db = TinyDB(os.getenv('DBFILEPATH'))
    db2 = TinyDB(os.getenv('DB2FILEPATH'))
    img_file_path = os.getenv('IMGFILEPATH')
    data = create_dict(filepath)
    for key, value in data.items():
        if not check_dup(db, key) and not check_dup(db2, key):
            print(f"Found new record, inserting {key}")
            prompt = create_vertex_prompt(key, value)
            output_file = re.sub('[^A-Za-z0-9]+', '', key)
            write_path = f"{img_file_path}{output_file}.png"
            choice = False
            while choice is False:
                create_vertex_image(prompt, write_path)
                reduceTool(write_path)
                im = Image.open(write_path)
                im.show()
                choice = click.confirm('Do you want to keep the displayed image?', default =True)
            print(f"SUCCESS: SAVED {key} to: {write_path}.")
            db.insert({'title': key, 'body': value})

if __name__=="__main__":
    add_items_to_db()
