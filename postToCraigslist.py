import os
import asyncio
import re
from dotenv import load_dotenv
from utils.postUtils import post
from utils.dbUtils import getPostFromDb, deletePostFromDb

async def main():
    listing = getPostFromDb()
    await post(listing)
    deletePostFromDb(listing)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())

