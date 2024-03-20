import os
import re
from tinydb import TinyDB
from dotenv import load_dotenv
from utils.parseUtils import create_dict, _parse_line, check_dup
from image_creator.stable_diffusion_openvino.makeImage import makeImage, reduceTool

def addItemsToDb():
    load_dotenv()
    filepath = os.getenv('TXTFILEPATH')
    db = TinyDB(os.getenv('DBFILEPATH'))
    db2 = TinyDB(os.getenv('DB2FILEPATH'))
    img_file_path = os.getenv('IMGFILEPATH')
    data = create_dict(filepath)
    img_key_array = []
    for key, value in data.items():
        if not check_dup(db, key) and not check_dup(db2, key):
            print(f"Found new record, inserting {key}")
            img_key_array.append(key)
            db.insert({'title': key, 'body': value})
    for img_key in img_key_array:
        output_file = re.sub('[^A-Za-z0-9]+', '', img_key)
        write_path = f"{img_file_path}{output_file}.png"
        makeImage(f"{img_key}, homemade photo, amateur photo, cellphone photograph", None, None, write_path)
        reduceTool(write_path)
                  
def main():
    addItemsToDb()

if __name__=="__main__":
    main()