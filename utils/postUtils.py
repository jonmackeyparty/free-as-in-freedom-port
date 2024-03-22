import os
import time 
import random
import re
import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import Page, expect, sync_playwright
from utils.mailUtils import getLink, sendLink, get_email_data, list_new_message

ZIPS = {"bronx": [10453, 10457, 10460, 10458, 10467, 10468, 10451, 10452, 10456, 10454, 10455, 10459, 10474, 10463, 10471, 10466, 10469, 10470, 10475, 10461, 10462,10464, 10465, 10472, 10473], "brooklyn": [11212, 11213, 11216, 11233, 11238, 11209, 11214, 11228, 11204, 11218, 11219, 11230, 11234, 11236, 11239, 11223, 11224, 11229, 11235, 11201, 11205, 11215, 11217, 11231, 11203, 11210, 11225, 11226, 11207, 11208, 11211, 11222, 11220, 11232, 11206, 11221, 11237], "queens": [11361, 11362, 11363, 11364, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11365, 11366, 11367, 11412, 11423, 11432, 11433, 11434, 11435, 11436, 11101, 11102, 11103, 11104, 11105, 11106, 11374, 11375, 11379, 11385, 11691, 11692, 11693, 11694, 11695, 11697, 11004, 11005, 11411, 11413, 11422, 11426, 11427, 11428, 11429, 11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421, 11368, 11369, 11370, 11372, 11373, 11377, 11378], "staten island": [10302, 10303, 10310, 10306, 10307, 10308, 10309, 10312, 10301, 10304, 10305, 10314]}

# # Define the SCOPES. If modifying it, delete the token.pickle file. 
# SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"] 

class newPost:
    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.borough = random.choice(list(ZIPS.keys()))
        self.zip = random.choice(ZIPS[self.borough])

async def logInAndPost(link, listing, filepath):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await browser.new_page()
        try:
            state = "Initial Login"
            await page.goto(link)
            await page.get_by_role('combobox').select_option(value='nyc')
            await page.get_by_role('button', name='go').click()
            if page.url.endswith("copyfromanother"):
                await page.get_by_role("button", name="skip").click()
                await page.locator("#ui-id-1-button").get_by_text("new york city").click()
                await page.get_by_role("option", name="new york city").click()
                await page.get_by_role("button", name="continue").click()
                await page.get_by_text(listing.borough).click()
                state = "ReUse Screen"
            else:
                await page.get_by_text(listing.borough).click()
                state = "Borough Select Screen"
            if listing.borough == 'manhattan':
                await page.get_by_text("bypass this step").click()
                state = "Manhattan Subregion Screen"
            await page.get_by_text('for sale by owner').click()
            await page.get_by_text('free stuff').click()
            await page.get_by_label('posting title').fill(listing.title)
            await page.get_by_label('description').fill(listing.body)
            await page.get_by_label('ZIP code').fill(str(listing.zip))
            await page.get_by_role('button', name='continue').click()
            state = "Post Form"
            await page.get_by_role('button', name='continue').click()
            state = "Location Confirmation Screen"
            #Image Selection - new feature
            async with page.expect_file_chooser() as fc_info:
                await page.get_by_role("button", name="Add Images").click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(filepath)
            await page.get_by_role("button", name="done with images").click()
            state= "Image Selection Screen"
            await page.locator("#publish_top").get_by_role("button", name="publish").click()
            state = "Post Confirmation Screen"
            post_link = await page.get_by_role("listitem").filter(has_text="View your post at").get_by_role("link").get_attribute('href')
            page_1 = await context.new_page()
            await page_1.goto(post_link)
            try:
                state = "Post Screenshot"
                await page_1.set_viewport_size({'width': 479, 'height': 959})
                await page_1.screenshot(path=f"./screenshots/{listing.title}.png")
                print(f"SUCCESS: {listing.title} POSTED AT {post_link}")
            except Exception as e:
                await page.screenshot(path="./screenshots/ERROR.png")
                print(f"An error occurred: {str(e)} Failed at {state}, see attached screenshot")
                raise
        except Exception as e:
            await page.screenshot(path="./screenshots/ERROR.png")
            print(f"An error occurred: {str(e)} Failed at {state}, see attached screenshot")
            raise
        print(f"SUCCESS: {listing.title} POSTED. CHECK SCREENSHOTS")
        await browser.close()
        return(post_link)

async def post(listing, filepath):
    await sendLink()
    time.sleep(30)
    link = getLink()
    post_link = await logInAndPost(link, listing, filepath)
    return post_link

  
