import os
import re
import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import Page, expect, sync_playwright

async def logInAndPost(link, listing):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            await page.goto(link)
            await page.get_by_label(' new posting in: ').select_option(value='nyc')
            await page.get_by_role("button", value="go").click()
            await page.screenshot(path="MAINPAGE.png")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            await page.close()

