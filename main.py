from fastapi import FastAPI, Body, Path, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List
from starlette.requests import Request
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
import pymongo
from pymongo import MongoClient
from bson import ObjectId
from Models.models import Victima, Asesinato

client = pymongo.MongoClient('mongodb+srv://gastonmetzgera:yoloswagfear123@cluster0.7fnfgrt.mongodb.net/?retryWrites=true&w=majority')

db = client["biblioteca"]
libros_collection = db["libros"]
autores_collection = db["autores"]

app = FastAPI()
app.title = "Biblioteca API"
app.description = "API para la gestión de libros y autores en una biblioteca"

# Modelos Pydantic para libros y autores
class Libro(BaseModel):
    titulo: str
    autor_id: str

class Autor(BaseModel):
    nombre: str

# Operaciones CRUD para autores

# Registrar un nuevo autor
@app.post("/autores", tags=['Autores'])
def registrar_autor(autor: Autor):
    autor_id = autores_collection.insert_one(autor.dict()).inserted_id
    return {"message": "Autor registrado", "autor_id": str(autor_id)}

# Obtener todos los autores
@app.get("/autores", tags=['Autores'])
def obtener_autores():
    autores = list(autores_collection.find({}))
    if autores:
        for autor in autores:
            autor["_id"] = str(autor["_id"])
        return autores
    else:
        return {"message": "Sin autores encontrados"}

# Obtener un autor por su ID
@app.get("/autores/{id}", tags=['Autores'])
def obtener_autor(id: str):
    autor = autores_collection.find_one({"_id": ObjectId(id)})
    if autor:
        autor["_id"] = str(autor["_id"])
        return autor
    else:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

# Actualizar un autor por su ID
@app.put("/autores/{id}", tags=['Autores'])
def actualizar_autor(id: str, autor: Autor):
    autor_actualizado = autores_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": autor.dict()},
        return_document=True
    )
    if autor_actualizado:
        autor_actualizado["_id"] = str(autor_actualizado["_id"])
        return {"message": "Autor actualizado", "autor": autor_actualizado}
    else:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

# Eliminar un autor por su ID
@app.delete("/autores/{id}", tags=['Autores'])
def eliminar_autor(id: str):
    autor = autores_collection.find_one_and_delete({"_id": ObjectId(id)})
    if autor:
        return {"message": "Autor eliminado"}
    else:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

# Operaciones CRUD para libros

# Registrar un nuevo libro
@app.post("/libros", tags=['Libros'])
def registrar_libro(libro: Libro):
    autor = autores_collection.find_one({"_id": ObjectId(libro.autor_id)})
    if autor:
        libro_id = libros_collection.insert_one(libro.dict()).inserted_id
        return {"message": "Libro registrado", "libro_id": str(libro_id)}
    else:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

# Obtener todos los libros
@app.get("/libros", tags=['Libros'])
def obtener_libros():
    libros = list(libros_collection.find({}))
    if libros:
        for libro in libros:
            libro["_id"] = str(libro["_id"])
        return libros
    else:
        return {"message": "Sin libros encontrados"}

# Obtener un libro por su ID
@app.get("/libros/{id}", tags=['Libros'])
def obtener_libro(id: str):
    libro = libros_collection.find_one({"_id": ObjectId(id)})
    if libro:
        libro["_id"] = str(libro["_id"])
        return libro
    else:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

# Actualizar un libro por su ID
@app.put("/libros/{id}", tags=['Libros'])
def actualizar_libro(id: str, libro: Libro):
    autor = autores_collection.find_one({"_id": ObjectId(libro.autor_id)})
    if autor:
        libro_actualizado = libros_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": libro.dict()},
            return_document=True
        )
        if libro_actualizado:
            libro_actualizado["_id"] = str(libro_actualizado["_id"])
            return {"message": "Libro actualizado", "libro": libro_actualizado}
        else:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
    else:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

# Eliminar un libro por su ID
@app.delete("/libros/{id}", tags=['Libros'])
def eliminar_libro(id: str):
    libro = libros_collection.find_one_and_delete({"_id": ObjectId(id)})
    if libro:
        return {"message": "Libro eliminado"}
    else:
        raise HTTPException(status_code=404, detail="Libro no encontrado")