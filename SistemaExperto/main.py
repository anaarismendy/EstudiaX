"""Módulo principal de la API del sistema experto académico.

Expone endpoints HTTP usando FastAPI para interactuar con el motor de
reglas definido en `SistemaExperto_Clips` y evaluar el riesgo académico
de un estudiante a partir de sus datos.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from SistemaExperto_Clips import evaluar_riesgo


app = FastAPI()


# ---------------------------
# Configuración CORS
# ---------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción especificar dominios concretos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DatosEstudiante(BaseModel):
    """Modelo de datos de entrada que recibe la API.

    Representa la información relevante de un estudiante que será
    analizada por el sistema experto para determinar su nivel de riesgo.
    """

    promedio: float
    inasistencias: int
    participacion: int
    horas_estudio: float


@app.get("/")
def inicio():
    """Endpoint de verificación de estado de la API.

    Permite comprobar rápidamente que el servicio FastAPI está activo
    y respondiendo a las solicitudes HTTP.
    """

    return {"mensaje": "API Sistema Experto Académico Activa"}


@app.post("/evaluar-riesgo")
def evaluar(datos: DatosEstudiante):
    """Evalúa el nivel de riesgo académico de un estudiante.

    Recibe un objeto `DatosEstudiante` con la información necesaria,
    delega el análisis a la función `evaluar_riesgo` del sistema experto
    basado en CLIPS y devuelve el nivel de riesgo resultante.
    """

    resultado = evaluar_riesgo(
        datos.promedio,
        datos.inasistencias,
        datos.participacion,
        datos.horas_estudio,
    )

    return {
        "nivel_riesgo": resultado
    }