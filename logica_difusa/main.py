from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from logicaDifusa import calcular_nivel_estres
import os

app = FastAPI(title="Evaluador de Estrés Académico")

current_dir = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(current_dir, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def home():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/evaluar")
def evaluar(sueno: int, carga: int, ansiedad: int):
    val_fuzzy = calcular_nivel_estres(sueno, carga, ansiedad)
    
    # Clasificación por umbrales para el Frontend
    if val_fuzzy < 35:
        nivel = "Leve"
    elif val_fuzzy < 65:
        nivel = "Moderado"
    else:
        nivel = "Alto"
        
    return {"nivel": nivel}