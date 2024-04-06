import os
import asyncio
import re
import time
import multiprocessing
from dotenv import load_dotenv
from tinydb import TinyDB
from utils.postUtils import post
from utils.dbUtils import getPostFromDb, deletePostFromDb
from utils.textUtils import ngrok_server, send_twilio_with_image

async def main():
    load_dotenv()
    db = TinyDB(os.getenv('DBFILEPATH'))
    db2 = TinyDB(os.getenv('DB2FILEPATH'))
    img_file_path = os.getenv('IMGFILEPATH')
    screenshot_file_path = os.getenv('SCREENSHOTFILEPATH')
    ngrok_url = os.getenv('NGROK_DOMAIN')
    listing = getPostFromDb(db)
    output_file = re.sub('[^A-Za-z0-9]+', '', listing.title)
    filename = f"{output_file}.png"
    write_path = f"{img_file_path}{filename}"
    post_link = await post(listing, write_path)
    deletePostFromDb(db, db2, listing)
    print(f"Attempting to text the following file: {ngrok_url}{filename}")
    p1 = multiprocessing.Process(target=ngrok_server)
    p2 = multiprocessing.Process(target=send_twilio_with_image, args=(listing.title, f"{ngrok_url}{filename}"))
    p1.start()
    time.sleep(10)
    p2.start()
    
if __name__ == "__main__":
    asyncio.run(main())

