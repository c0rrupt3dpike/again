import random
import string
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db, engine, Base
from models import ShortenedURL, LinkToShorten
from fastapi.responses import RedirectResponse

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown tasks."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Application runs here
    await engine.dispose()  # Cleanup on shutdown

app = FastAPI(lifespan=lifespan)
        


async def short_code_generate(db: AsyncSession) -> str:
    short_code =  ''.join(random.choices(string.ascii_letters, k=5))
    result = await db.execute(select(ShortenedURL).where(ShortenedURL.short_code == short_code))
    if result.scalars().first() is None:
        return short_code
    

@app.get("/")
async def root():
    return{"message: sup fam"}

@app.post("/linkshortener/")
async def link_shortener(link_to_shorten: LinkToShorten, db: AsyncSession = Depends(get_db)):
    short_code = await short_code_generate(db)

    short_link = ShortenedURL(original_url=link_to_shorten.link, short_code=short_code)
    db.add(short_link)
    await db.commit()
    return {"Ur shortened link": f"http://127.0.0.1:8000/{short_code}"}

@app.get("/{short_code}")
async def get_link(short_code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ShortenedURL).where(ShortenedURL.short_code == short_code))
    url_entry = result.scalars().first()

    if url_entry is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    url_entry.redirect_count += 1
    await db.commit()
    await db.refresh(url_entry)
    return RedirectResponse(url=url_entry.original_url)
