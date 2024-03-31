import os
import time
import re
import multiprocessing
from dotenv import load_dotenv
from tinydb import TinyDB
from utils.dbUtils import getPostFromDb
from utils.textUtils import ngrok_server, send_twilio_with_image

def main():
    load_dotenv()
    db = TinyDB(os.getenv('DB2FILEPATH'))
    ngrok_url = os.getenv('NGROK_DOMAIN')
    listing = getPostFromDb(db)
    output_file = re.sub('[^A-Za-z0-9]+', '', listing.title)
    filename = f"{output_file}.png"
    print(f"Attempting to text the following file: {ngrok_url}{filename}")
    p1 = multiprocessing.Process(target=ngrok_server)
    p2 = multiprocessing.Process(target=send_twilio_with_image, args=(listing.title, f"{ngrok_url}{filename}"))
    p1.start()
    time.sleep(15)
    p2.start()

if __name__ == '__main__':
    # freeze_support()
    main()