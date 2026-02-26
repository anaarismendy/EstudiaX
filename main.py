"""
API Unificada:
- Evaluador de Estrés (Lógica Difusa)
- Sistema Experto Académico
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles


# Importaciones de tus módulos
from logica_difusa.logicaDifusa import calcular_nivel_estres
from SistemaExperto.SistemaExperto import evaluar_riesgo


app = FastAPI(title="Sistema Académico Inteligente")

# ---------------------------
# Configuración CORS
# ---------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción especificar dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# MODELOS
# ---------------------------

class DatosEstudiante(BaseModel):
    promedio: float
    inasistencias: int
    participacion: int
    horas_estudio: float


# ---------------------------
# ENDPOINT GENERAL
# ---------------------------

@app.get("/")
def home():
    return {
        "mensaje": "API Sistema Académico Inteligente Activa",
        "endpoints": {
            "estres": "/evaluar-estres",
            "riesgo": "/evaluar-riesgo"
        }
    }


# ==========================================================
# 🔵 LÓGICA DIFUSA – EVALUADOR DE ESTRÉS
# ==========================================================

@app.get("/evaluar-estres")
def evaluar_estres(sueno: int, carga: int, ansiedad: int):

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


# ==========================================================
# 🟢 SISTEMA EXPERTO – RIESGO ACADÉMICO
# ==========================================================

@app.post("/evaluar-riesgo")
def evaluar(datos: DatosEstudiante):

    resultado = evaluar_riesgo(
        datos.promedio,
        datos.inasistencias,
        datos.participacion,
        datos.horas_estudio,
    )

    return {
        "nivel_riesgo": resultado
    }

app.mount("/", StaticFiles(directory="public", html=True), name="static")
