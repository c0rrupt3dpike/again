from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
import random
import string
from fastapi.responses import RedirectResponse

app = FastAPI()

class LinkToShorten(BaseModel):
    link:str

short_links = {}

def link_short(link: str):
    random_letters = ''.join(random.choices(string.ascii_letters, k=5))
    short_links[random_letters] = link
    print(short_links[random_letters])
    return random_letters

@app.get("/")
async def root():
    return{"message: sup fam"}

@app.post("/linkshortener/")
async def link_shortener(link_to_shorten: LinkToShorten):
    short_link = link_short(link_to_shorten.link)
    return {"Ur shortened link": f"http://127.0.0.1:8000/{short_link}"}

@app.get("/{short_link}")
async def get_link(short_link: str):
    destination = short_links.get(short_link)
    print(destination)
    return RedirectResponse(url=destination)
