import re
import os
from tinydb import TinyDB, Query
from dotenv import load_dotenv


load_dotenv()
db = TinyDB(os.getenv('DBFILEPATH'))
rx_dict = {
    'TITLE': re.compile(r'.*(?=BODY:)'),
    'BODY': re.compile(r'(?<=BODY:).*')
}

def _parse_line(line, arr1, arr2):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            if key == 'TITLE':
                arr1.append(match.group())
            if key == 'BODY':
                arr2.append(match.group())
    return arr1, arr2

def create_dict(filepath):
    titles = []
    descriptions = []
    with open(filepath, 'r') as file_object:
        file_contents = file_object.read()
        file_contents = ''.join(file_contents.splitlines())
        file_contents_array = file_contents.split('TITLE:')
        for entry in file_contents_array:
            _parse_line(entry, titles, descriptions)
    return dict(zip(titles, descriptions))

def add_items_to_db(filepath):
    db = TinyDB('listings.json')
    data = create_dict(filepath)
    for key, value in data.items():
        if not check_dup(key):
            db.insert({'title': key, 'body': value})

def check_dup(key):
    listing = Query()
    return db.search(listing.title == key)

filepath = os.getenv('TXTFILEPATH')
add_items_to_db(filepath)



            