from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logica_difusa.logicaDifusa import calcular_nivel_estres

app = FastAPI(title="Evaluador de Estrés Académico")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se pone la URL específica
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensaje": "API Evaluador de Estrés activa"}

@app.get("/evaluar")
def evaluar(sueno: int, carga: int, ansiedad: int):
    val_fuzzy = calcular_nivel_estres(sueno, carga, ansiedad)

    if val_fuzzy < 35:
        nivel = "Leve"
    elif val_fuzzy < 65:
        nivel = "Moderado"
    else:
        nivel = "Alto"

    return {
        "valor_fuzzy": round(val_fuzzy, 2),
        "nivel": nivel
    }