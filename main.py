"""
API Unificada:
- Evaluador de Estrés (Lógica Difusa)
- Sistema Experto Académico
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from logica_difusa.logicaDifusa import calcular_nivel_estres
from SistemaExperto.SistemaExperto import evaluar_riesgo

app = FastAPI(title="Sistema Académico Inteligente")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DatosEstudiante(BaseModel):
    promedio: float
    inasistencias: int
    participacion: int
    horas_estudio: float

# ==========================================================
# 🔵 LÓGICA DIFUSA – EVALUADOR DE ESTRÉS
# ==========================================================

@app.get("/api/evaluar-estres")
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

@app.post("/api/evaluar-riesgo")
def evaluar(datos: DatosEstudiante):
    resultado = evaluar_riesgo(
        datos.promedio,
        datos.inasistencias,
        datos.participacion,
        datos.horas_estudio,
    )
    return {"nivel_riesgo": resultado}

# ✅ Sin endpoint en "/" — StaticFiles sirve el index.html directamente
app.mount("/", StaticFiles(directory="public", html=True), name="static")