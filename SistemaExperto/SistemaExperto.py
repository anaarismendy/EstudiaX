"""
Motor de reglas CLIPS para evaluar riesgo académico.

Este módulo encapsula la integración con CLIPS mediante la librería
`clipspy`. Define las plantillas (`deftemplate`) y reglas (`defrule`)
necesarias para clasificar a un estudiante en diferentes niveles de
riesgo académico (alto, medio, bajo) según sus datos.

Se garantiza que siempre se genere un resultado, evitando el estado
"No determinado" mediante una regla por defecto.
"""

import clips


def evaluar_riesgo(promedio, inasistencias, participacion, horas_estudio):
    """
    Evalúa el nivel de riesgo académico de un estudiante.

    Se crea un entorno CLIPS aislado por evaluación. Se definen las
    plantillas de hechos y reglas de inferencia. Luego se inserta un
    hecho `estudiante` con los datos proporcionados y se ejecuta el
    motor de inferencia para obtener un hecho `resultado`.

    Parámetros
    ----------
    promedio : float
        Promedio numérico del estudiante.
    inasistencias : int
        Número de inasistencias registradas.
    participacion : int
        Nivel de participación.
    horas_estudio : float
        Cantidad de horas de estudio.

    Retorna
    -------
    str
        Nivel de riesgo calculado:
        - "Alto riesgo"
        - "Riesgo medio"
        - "Bajo riesgo"

    Nota
    ----
    Siempre se devuelve un nivel de riesgo. Se incluye una regla
    por defecto que garantiza que el sistema no quede sin clasificar.
    """

    # Crear entorno CLIPS aislado
    env = clips.Environment()

    # -----------------------------------------------------------------
    # Plantillas de hechos
    # -----------------------------------------------------------------

    env.build("""
        (deftemplate estudiante
            (slot promedio)
            (slot inasistencias)
            (slot participacion)
            (slot horas_estudio)
        )
    """)

    env.build("""
        (deftemplate resultado
            (slot nivel)
        )
    """)

    # -----------------------------------------------------------------
    # Reglas de inferencia
    # -----------------------------------------------------------------

    # -------------------------
    # ALTO RIESGO
    # -------------------------

    env.build("""
        (defrule regla-alto-riesgo
            (estudiante
                (promedio ?p&:(< ?p 3.0))
                (inasistencias ?i&:(> ?i 8))
            )
            =>
            (assert (resultado (nivel "Alto riesgo")))
        )
    """)

    env.build("""
        (defrule regla-alto-riesgo-estudio
            (estudiante
                (horas_estudio ?h&:(< ?h 3))
                (participacion ?pa&:(<= ?pa 4))
            )
            =>
            (assert (resultado (nivel "Alto riesgo")))
        )
    """)

    # -------------------------
    # RIESGO MEDIO
    # -------------------------

    env.build("""
        (defrule regla-riesgo-medio
            (estudiante
                (promedio ?p&:(< ?p 3.5))
                (inasistencias ?i&:(> ?i 4))
            )
            =>
            (assert (resultado (nivel "Riesgo medio")))
        )
    """)

    env.build("""
        (defrule regla-riesgo-medio-estudio
            (estudiante
                (horas_estudio ?h&:(< ?h 6))
            )
            =>
            (assert (resultado (nivel "Riesgo medio")))
        )
    """)

    # -------------------------
    # BAJO RIESGO
    # -------------------------

    env.build("""
        (defrule regla-bajo-riesgo
            (estudiante
                (promedio ?p&:(>= ?p 3.5))
                (inasistencias ?i&:(<= ?i 4))
                (horas_estudio ?h&:(>= ?h 6))
            )
            =>
            (assert (resultado (nivel "Bajo riesgo")))
        )
    """)

    # -----------------------------------------------------------------
    # REGLA POR DEFECTO (GARANTIZA CLASIFICACIÓN)
    # -----------------------------------------------------------------
    # Esta regla solo se dispara si NO existe ningún hecho 'resultado'.
    # Se utiliza la condición (not (resultado ...)) para verificarlo.
    # Se asigna por defecto "Riesgo medio" como clasificación neutral.

    env.build("""
        (defrule regla-por-defecto
            (declare (salience -10))
            (estudiante)
            (not (resultado))
            =>
            (assert (resultado (nivel "Riesgo medio")))
        )
    """)

    # -----------------------------------------------------------------
    # Inserción del hecho inicial
    # -----------------------------------------------------------------

    env.assert_string(f"""
        (estudiante
            (promedio {promedio})
            (inasistencias {inasistencias})
            (participacion {participacion})
            (horas_estudio {horas_estudio})
        )
    """)

    # Ejecutar motor de inferencia
    env.run()

    # -----------------------------------------------------------------
    # Recuperar resultados
    # -----------------------------------------------------------------

    resultados = []

    for fact in env.facts():
        if fact.template.name == "resultado":
            resultados.append(fact["nivel"])

    # Priorización jerárquica de resultados
    if "Alto riesgo" in resultados:
        return "Alto riesgo"
    elif "Riesgo medio" in resultados:
        return "Riesgo medio"
    else:
        return "Bajo riesgo"