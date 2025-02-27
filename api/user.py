from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.database import SessionLocal, engine
from api.models import Usuario, Album, Cancion

router = APIRouter()

class UserLogin(BaseModel):
    correo: str
    contrasena: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/user/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.correo == user.correo).first()
    if db_user is None or db_user.contrasena != user.contrasena:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {
        "id": db_user.id,
        "nombre": db_user.nombre,
        "correo": db_user.correo,
        "albums": [
            {
                "id": album.id,
                "nombre": album.nombre,
                "canciones": [
                    {
                        "id": cancion.id,
                        "nombre": cancion.nombre,
                        "artista": cancion.artista,
                        "url": cancion.url,
                        "image_url": cancion.image_url
                    }
                    for cancion in album.canciones
                ]
            }
            for album in db_user.albums
        ]
    }

@router.get("/user/{id}/albums")
def get_user_albums(id: int, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return [
        {
            "id": album.id,
            "nombre": album.nombre,
            "canciones": [
                {
                    "id": cancion.id,
                    "nombre": cancion.nombre,
                    "artista": cancion.artista,
                    "url": cancion.url,
                    "image_url": cancion.image_url
                }
                for cancion in album.canciones
            ]
        }
        for album in db_user.albums
    ]


