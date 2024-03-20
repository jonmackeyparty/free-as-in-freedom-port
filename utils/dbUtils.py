import os
import random
from tinydb import TinyDB, Query
from utils.postUtils import newPost

def getPostFromDb(db):
    ind = random.randint(0,len(db))
    title = db.all()[ind]['title']
    body = db.all()[ind]['body']
    return newPost(title, body)

def deletePostFromDb(db, db2, listing):
    print(f"Removing {listing.title}...")
    db2.insert({'title': listing.title, 'body': listing.body})
    Post = Query()
    db.remove(Post.title == listing.title)
