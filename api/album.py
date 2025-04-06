from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import Album, Cancion

router = APIRouter()

class AlbumCreate(BaseModel):
    nombre: str
    id_usuario: int

class AlbumUpdate(BaseModel):
    nombre: str

class CancionCreate(BaseModel):
    id: str
    name: str
    artist: str
    url: str
    image_url: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/album/")
def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
    db_album = Album(nombre=album.nombre, id_usuario=album.id_usuario)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

@router.put("/album/{album_id}")
def update_album(album_id: int, album: AlbumUpdate, db: Session = Depends(get_db)):
    db_album = db.query(Album).filter(Album.id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    db_album.nombre = album.nombre
    db.commit()
    db.refresh(db_album)
    return db_album

@router.delete("/album/{album_id}")
def delete_album(album_id: int, db: Session = Depends(get_db)):
    db_album = db.query(Album).filter(Album.id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    db.delete(db_album)
    db.commit()
    return {"detail": "Album deleted"}

@router.post("/album/{album_id}/cancion")
def add_cancion_to_album(album_id: int, cancion: CancionCreate, db: Session = Depends(get_db)):
    db_album = db.query(Album).filter(Album.id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    db_cancion = Cancion(id=cancion.id, nombre=cancion.nombre, artista=cancion.artista, url=cancion.url, image_url=cancion.image_url, id_album=album_id)
    db.add(db_cancion)
    db.commit()
    db.refresh(db_cancion)
    return db_cancion

@router.delete("/album/{album_id}/cancion/{cancion_id}")
def delete_cancion_from_album(album_id: int, cancion_id: str, db: Session = Depends(get_db)):
    db_cancion = db.query(Cancion).filter(Cancion.id == cancion_id, Cancion.id_album == album_id).first()
    if db_cancion is None:
        raise HTTPException(status_code=404, detail="Cancion not found")
    db.delete(db_cancion)
    db.commit()
    return {"detail": "Cancion deleted"}
