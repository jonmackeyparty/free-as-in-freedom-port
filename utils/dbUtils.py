import os
import random
from dotenv import load_dotenv
from tinydb import TinyDB, Query
from postUtils import newPost

load_dotenv()
DB = TinyDB(os.getenv('DBFILEPATH'))

def getPostFromDb():
    ind = random.randint(0,len(DB))
    title = DB.all()[ind]['title']
    body = DB.all()[ind]['body']
    return newPost(title, body)

def deletePostFromDb(listing):
    print(f"Removing {listing.title}...")
    Post = Query()
    DB.remove(Post.title == listing.title)