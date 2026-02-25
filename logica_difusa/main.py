from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from logicaDifusa import calcular_nivel_estres
import os

app = FastAPI(title="API de Estrés Académico")

# Montamos la carpeta static para que FastAPI pueda leer el HTML
# Asegúrate de que la ruta sea correcta
current_dir = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(current_dir, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def home():
    # Esto hará que al entrar a http://127.0.0.1:8000 se abra el HTML automáticamente
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/evaluar")
def evaluar(sueno: int, carga: int, ansiedad: int):
    resultado_num = calcular_nivel_estres(sueno, carga, ansiedad)
    
    if resultado_num < 40:
        categoria = "Bajo"
    elif resultado_num < 70:
        categoria = "Moderado"
    else:
        categoria = "Alto"
        
    return {
        "score_estres": round(resultado_num, 2),
        "nivel": categoria
    }