from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
import random
import string
from fastapi.responses import RedirectResponse

app = FastAPI()



class ModelName(str, Enum):
    cnn="cnn"
    catboost="catboost"
    gradient="gradient"

short_links = {}

def link_short(link: str):
    random_letters = ''.join(random.choices(string.ascii_letters, k=5))
    short_links[random_letters] = link
    print(short_links[random_letters])
    return random_letters


@app.get("/")
async def root():
    return{"message: sup fam"}

@app.get("/users")
async def read_users1():
    return ["admin", "pops"]

@app.get("/users")
async def read_users2():
    return ["pops", "other lad"]

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}, {"item:name": "Tuz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.get("/users/{user_id}/tracks/{track_id}")
async def track(user_id: int, track_id: str, q: str | None = None, short: bool=False):
    track = {"track_id": track_id, "Musician": user_id,}

    if q:
        track.update({"q": q})
    if not short:
        track.update(
            {"description": "This is an amazing track that has a long description"}
        )
    return track

@app.get("/buses/{buses_id}")
async def bus(buses_id: int):
    buspath = {"1": "Goes to Kapchagai",
       "2": "Goes to Opera",
       "3": "Goes nahui(Chimkent)"
       }
    if buses_id not in buspath.keys():
        return{"message": "Совсем башкой тронулся"}
    return{f"Where goes {buses_id}": buspath[buses_id]}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/loads/{loads_id}")
async def read_loads(loads_id: str, required: str):
    bag={"item_id": loads_id, "needy": required}
    return bag


@app.get("/counts/{model_name}")
async def read_models(model_name: ModelName):
    if model_name is ModelName.cnn:
        return {"model_name": model_name, "message": "Deep Learning model"}
    
    if model_name.value == "catboost":
        return {"model_name": model_name, "message": "Boosting from yandex"}
    
    return {"model_name": model_name, "message": "Have some residuals"}


class LinkToShorten(BaseModel):
    link:str

@app.post("/linkshortener/")
async def link_shortener(link_to_shorten: LinkToShorten):
    short_link = link_short(link_to_shorten.link)
    return {"Ur shortened link": f"http://127.0.0.1:8000/{short_link}"}

@app.get("/{short_link}")
async def get_link(short_link: str):
    destination = short_links.get(short_link)
    print(destination)
    return RedirectResponse(url=destination)
