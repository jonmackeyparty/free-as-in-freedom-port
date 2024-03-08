import os
import re
import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import Page, expect, sync_playwright
from dotenv import load_dotenv

load_dotenv()
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto("http://accounts.craigslist.org/login")
            await page.get_by_label("Email / Handle").fill(os.environ.get('USER'))
            await page.get_by_label("Password").fill(os.environ.get('PASSWORD'))
            await page.get_by_role("button", name="Log in").click()
            await page.get_by_role("button", name="click here").click()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            await page.close()

asyncio.run(main())