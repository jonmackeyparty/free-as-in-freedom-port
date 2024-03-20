import os
import asyncio
import re
from dotenv import load_dotenv
from tinydb import TinyDB
from utils.postUtils import post
from utils.dbUtils import getPostFromDb, deletePostFromDb

async def main():
    load_dotenv()
    db = TinyDB(os.getenv('DBFILEPATH'))
    db2 = TinyDB(os.getenv('DB2FILEPATH'))
    img_file_path = os.getenv('IMGFILEPATH')
    listing = getPostFromDb(db)
    output_file = re.sub('[^A-Za-z0-9]+', '', listing.title)
    write_path = f"{img_file_path}{output_file}.png"
    await post(listing, write_path)
    deletePostFromDb(db, db2, listing)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
