import os
import datetime
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI()

# ---------- Config DB ----------

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

if DB_HOST and DB_NAME and DB_USER and DB_PASSWORD:
    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
else:
    # Fallback pour du dev local sans DB
    DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Création des tables au démarrage
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Schéma API ----------

class Item(BaseModel):
    id: int
    title: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items", response_model=List[Item])
def list_items(db: Session = Depends(get_db)):
    items = db.query(ItemDB).order_by(ItemDB.id).all()
    return items


@app.post("/items", response_model=Item, status_code=201)
def create_item(title: str, db: Session = Depends(get_db)):
    item = ItemDB(title=title)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return
