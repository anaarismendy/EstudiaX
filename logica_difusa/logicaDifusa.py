import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def calcular_nivel_estres(horas_sueno, num_materias, nivel_ansiedad):
    sueno = ctrl.Antecedent(np.arange(0, 13, 1), 'sueno')
    carga = ctrl.Antecedent(np.arange(1, 11, 1), 'carga')
    ansiedad = ctrl.Antecedent(np.arange(0, 11, 1), 'ansiedad')
    estres = ctrl.Consequent(np.arange(0, 101, 1), 'estres')

    # Rediseño de rangos: El sueño "Poco" ahora es más crítico (0-4 horas)
    sueno['poco'] = fuzz.trapmf(sueno.universe, [0, 0, 1, 5])
    sueno['adecuado'] = fuzz.trimf(sueno.universe, [4, 7, 9])
    sueno['bueno'] = fuzz.trapmf(sueno.universe, [8, 10, 12, 12])

    carga['baja'] = fuzz.trapmf(carga.universe, [1, 1, 2, 5])
    carga['media'] = fuzz.trimf(carga.universe, [4, 6, 8])
    carga['alta'] = fuzz.trapmf(carga.universe, [7, 9, 10, 10])

    ansiedad['bajo'] = fuzz.trapmf(ansiedad.universe, [0, 0, 1, 4])
    ansiedad['medio'] = fuzz.trimf(ansiedad.universe, [3, 5, 7])
    ansiedad['alto'] = fuzz.trapmf(ansiedad.universe, [6, 8, 10, 10])

    # Salidas más marcadas
    estres['bajo'] = fuzz.trapmf(estres.universe, [0, 0, 15, 35])
    estres['moderado'] = fuzz.trimf(estres.universe, [30, 50, 70])
    estres['alto'] = fuzz.trapmf(estres.universe, [60, 80, 100, 100])

    # 3. REGLAS CON PRIORIDAD
    reglas = [
        # REGLAS CRÍTICAS (Si esto pasa, el estrés es ALTO sí o sí)
        ctrl.Rule(sueno['poco'], estres['alto']),
        ctrl.Rule(ansiedad['alto'], estres['alto']),
        ctrl.Rule(carga['alta'] & ansiedad['medio'], estres['alto']),
        
        # REGLAS MEDIAS
        ctrl.Rule(sueno['adecuado'] & carga['media'], estres['moderado']),
        ctrl.Rule(sueno['adecuado'] & ansiedad['medio'], estres['moderado']),
        ctrl.Rule(sueno['bueno'] & carga['alta'], estres['moderado']),

        # REGLAS BAJAS (Solo si todo está bien)
        ctrl.Rule(sueno['bueno'] & carga['baja'] & ansiedad['bajo'], estres['bajo']),
        ctrl.Rule(sueno['adecuado'] & carga['baja'] & ansiedad['bajo'], estres['bajo'])
    ]

    sistema_control = ctrl.ControlSystem(reglas)
    simulador = ctrl.ControlSystemSimulation(sistema_control)

    simulador.input['sueno'] = horas_sueno
    simulador.input['carga'] = num_materias
    simulador.input['ansiedad'] = nivel_ansiedad

    simulador.compute()
    return simulador.output['estres']