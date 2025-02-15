from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel
class LinkToShorten(BaseModel):
    link:str

class ShortenedURL(Base):
    __tablename__="shortened_urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index = True)
    redirect_count = Column(Integer, default=0)