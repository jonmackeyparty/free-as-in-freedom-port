import re
import os
from tinydb import TinyDB, Query

def _parse_line(line, arr1, arr2):
    rx_dict = {
        'TITLE': re.compile(r'.*(?=BODY:)'),
        'BODY': re.compile(r'(?<=BODY:).*')
    }
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

def check_dup(db, key):
    listing = Query()
    return db.search(listing.title == key)

def remove_child_terms(prompt):
    """Removes child terms from prompt"""
    child_terms = ['child', 'children', 'kid', 'kids', 'baby', 'babies']
    for term in child_terms:
        prompt = re.sub(r'\b' + term + r'\b', '', prompt)
    return prompt

            