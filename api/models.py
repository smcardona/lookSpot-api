from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from api.database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(100), nullable=False)
    albums = relationship("Album", back_populates="usuario")

class Album(Base):
    __tablename__ = "album"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="albums")
    canciones = relationship("Cancion", back_populates="album", cascade="all, delete-orphan")

class Cancion(Base):
    __tablename__ = "cancion"
    id = Column(String(50), primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    artista = Column(String(150), nullable=False)
    url = Column(Text, nullable=False)
    image_url = Column(Text, nullable=False)
    id_album = Column(Integer, ForeignKey("album.id"), nullable=False)
    
    # Remove `cascade="all, delete-orphan"` from this line
    album = relationship("Album", back_populates="canciones")
