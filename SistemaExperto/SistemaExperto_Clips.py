"""Motor de reglas CLIPS para evaluar riesgo académico.

Este módulo encapsula la integración con CLIPS mediante la librería
`clipspy`. Define las plantillas (`deftemplate`) y reglas (`defrule`)
necesarias para clasificar a un estudiante en diferentes niveles de
riesgo académico (alto, medio, bajo) según sus datos.
"""

import clips


def evaluar_riesgo(promedio, inasistencias, participacion, horas_estudio):
    """Evalúa el nivel de riesgo académico de un estudiante.

    Crea un entorno CLIPS, define las plantillas de hechos y las reglas
    de inferencia, inserta un hecho `estudiante` con los datos
    proporcionados y ejecuta el motor para obtener un hecho `resultado`
    con el nivel de riesgo.

    Parámetros
    ----------
    promedio : float
        Promedio numérico del estudiante.
    inasistencias : int
        Número de inasistencias registradas.
    participacion : int
        Nivel de participación (por ejemplo, en una escala definida por el sistema).
    horas_estudio : float
        Cantidad de horas de estudio (por día o semana, según el modelo).

    Devuelve
    --------
    str
        Cadena con el nivel de riesgo calculado: "Alto riesgo",
        "Riesgo medio", "Bajo riesgo" o "No determinado" si no se cumple
        ninguna regla.
    """

    # Crear un nuevo entorno CLIPS aislado por evaluación
    env = clips.Environment()

    # -----------------------------
    # Plantillas de hechos (deftemplate)
    # -----------------------------
    env.build(
        """
        (deftemplate estudiante
            (slot promedio)
            (slot inasistencias)
            (slot participacion)
            (slot horas_estudio)
        )
        """
    )

    env.build(
        """
        (deftemplate resultado
            (slot nivel)
        )
        """
    )

    # -----------------------------
    # Reglas de inferencia
    # -----------------------------

    # Alto riesgo: bajo promedio y muchas inasistencias
    env.build(
        """
        (defrule regla-alto-riesgo
            (estudiante
                (promedio ?p&:(< ?p 3.0))
                (inasistencias ?i&:(> ?i 8))
            )
            =>
            (assert (resultado (nivel "Alto riesgo")))
        )
        """
    )

    # Alto riesgo: pocas horas de estudio y baja participación
    env.build(
        """
        (defrule regla-alto-riesgo-estudio
            (estudiante
                (horas_estudio ?h&:(< ?h 3))
                (participacion ?pa&:(<= ?pa 4))
            )
            =>
            (assert (resultado (nivel "Alto riesgo")))
        )
        """
    )

    # Riesgo medio: promedio moderadamente bajo y algunas inasistencias
    env.build(
        """
        (defrule regla-riesgo-medio
            (estudiante
                (promedio ?p&:(< ?p 3.5))
                (inasistencias ?i&:(> ?i 4))
            )
            =>
            (assert (resultado (nivel "Riesgo medio")))
        )
        """
    )

    # Riesgo medio: horas de estudio por debajo del umbral
    env.build(
        """
        (defrule regla-riesgo-medio-estudio
            (estudiante
                (horas_estudio ?h&:(< ?h 6))
            )
            =>
            (assert (resultado (nivel "Riesgo medio")))
        )
        """
    )

    # Bajo riesgo: buen promedio, pocas inasistencias y suficientes horas de estudio
    env.build(
        """
        (defrule regla-bajo-riesgo
            (estudiante
                (promedio ?p&:(>= ?p 3.5))
                (inasistencias ?i&:(<= ?i 4))
                (horas_estudio ?h&:(>= ?h 6))
            )
            =>
            (assert (resultado (nivel "Bajo riesgo")))
        )
        """
    )

    # -----------------------------
    # Inserción de hechos iniciales
    # -----------------------------
    env.assert_string(
        f"""
        (estudiante
            (promedio {promedio})
            (inasistencias {inasistencias})
            (participacion {participacion})
            (horas_estudio {horas_estudio})
        )
        """
    )

    # Ejecutar el motor de inferencia para disparar las reglas aplicables
    env.run()

    # Recopilar todos los hechos `resultado` generados
    resultados = []
    for fact in env.facts():
        if fact.template.name == "resultado":
            resultados.append(fact["nivel"])

    if resultados:
        # Priorización: si hay algún "Alto riesgo" se devuelve ese valor,
        # en caso contrario "Riesgo medio" y, si no, "Bajo riesgo".
        if "Alto riesgo" in resultados:
            return "Alto riesgo"
        elif "Riesgo medio" in resultados:
            return "Riesgo medio"
        else:
            return "Bajo riesgo"

    # Si no se generó ningún hecho de resultado, el caso queda sin clasificar
    return "No determinado"