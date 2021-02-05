import asyncio
from io import BytesIO

import aiohttp
import pdf2image
from bs4 import BeautifulSoup
from vkbottle import PhotoMessageUploader

loop = asyncio.get_event_loop()
schedule_url = "https://ulpst.ru/studentam/raspisanie/"


def get_page_urls(html):
    return BeautifulSoup(html, "lxml").findAll(
        "a",
        class_="style_doc",
    )


async def get_course_url(course):
    async with aiohttp.ClientSession() as session:
        async with session.get(schedule_url) as response:
            html = await response.text()
            page_urls = await loop.run_in_executor(
                None,
                get_page_urls,
                html,
            )
    for url in page_urls:
        if course in url.text:
            return (
                url.text,
                "https://ulpst.ru/{}".format(url.get("href")),  # noqa: P101
            )


async def get_schedule_images(course_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(course_url) as response:
            b_object = await response.read()
            return await loop.run_in_executor(
                None,
                pdf2image.convert_from_bytes,
                b_object,
            )


async def upload(peer_id, api, images):
    uploader = PhotoMessageUploader(api)
    images_links = []
    for img in images:
        fp = BytesIO()
        img.save(fp, "png")
        link = await uploader.upload(fp, peer_id=peer_id)
        images_links.append(link)
    return images_links


async def get_schedule(peer_id, api, course):
    text, course_url = await get_course_url(course)
    images = await get_schedule_images(course_url)
    images_links = await upload(peer_id, api, images)
    return text, images_links
