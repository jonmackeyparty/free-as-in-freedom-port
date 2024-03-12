import os
import time 
import asyncio
import re
import random
from tinydb import TinyDB, Query
from dotenv import load_dotenv
from sendLink import sendLink
from getLink import getLink
from logInAndPost import logInAndPost

ZIPS = {"bronx": [10453, 10457, 10460, 10458, 10467, 10468, 10451, 10452, 10456, 10454, 10455, 10459, 10474, 10463, 10471, 10466, 10469, 10470, 10475, 10461, 10462,10464, 10465, 10472, 10473], "brooklyn": [11212, 11213, 11216, 11233, 11238, 11209, 11214, 11228, 11204, 11218, 11219, 11230, 11234, 11236, 11239, 11223, 11224, 11229, 11235, 11201, 11205, 11215, 11217, 11231, 11203, 11210, 11225, 11226, 11207, 11208, 11211, 11222, 11220, 11232, 11206, 11221, 11237], "queens": [11361, 11362, 11363, 11364, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11365, 11366, 11367, 11412, 11423, 11432, 11433, 11434, 11435, 11436, 11101, 11102, 11103, 11104, 11105, 11106, 11374, 11375, 11379, 11385, 11691, 11692, 11693, 11694, 11695, 11697, 11004, 11005, 11411, 11413, 11422, 11426, 11427, 11428, 11429, 11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421, 11368, 11369, 11370, 11372, 11373, 11377, 11378], "staten island": [10302, 10303, 10310, 10306, 10307, 10308, 10309, 10312, 10301, 10304, 10305, 10314]}
CRAIGS_ZIPS = {"bronx": 4, "brooklyn": 2, "manhattan": 1, "queens": 3, "staten island": 5}

class newPost:
    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.borough = random.choice(list(ZIPS.keys()))
        self.zip = random.choice(ZIPS[self.borough])
        self.radio_zip = CRAIGS_ZIPS[self.borough]

def getPostFromDb():
    db = TinyDB(os.getenv('DBFILEPATH'))
    ind = random.randint(0,len(db))
    title = db.all()[ind]['title']
    body = db.all()[ind]['body']
    return newPost(title, body)

async def start():
    listing = getPostFromDb()
    await sendLink()
    time.sleep(30)
    link = getLink()
    await logInAndPost(link, listing)

load_dotenv()
asyncio.run(start())
