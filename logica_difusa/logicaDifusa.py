import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def calcular_nivel_estres(horas_sueno, num_materias, nivel_ansiedad):

    # Definición de Variables

    sueno = ctrl.Antecedent(np.arange(0, 13, 1), 'sueno')
    carga = ctrl.Antecedent(np.arange(1, 11, 1), 'carga')
    ansiedad = ctrl.Antecedent(np.arange(0, 11, 1), 'ansiedad')
    estres = ctrl.Consequent(np.arange(0, 101, 1), 'estres')

    # Funciones de Pertenencia

    sueno['poco'] = fuzz.trapmf(sueno.universe, [0, 0, 2, 5])
    sueno['adecuado'] = fuzz.trimf(sueno.universe, [4, 7, 9])
    sueno['bueno'] = fuzz.trapmf(sueno.universe, [8, 10, 12, 12])

    carga['baja'] = fuzz.trapmf(carga.universe, [1, 1, 3, 5])
    carga['media'] = fuzz.trimf(carga.universe, [4, 6, 8])
    carga['alta'] = fuzz.trapmf(carga.universe, [7, 9, 10, 10])

    ansiedad['bajo'] = fuzz.trapmf(ansiedad.universe, [0, 0, 2, 5])
    ansiedad['medio'] = fuzz.trimf(ansiedad.universe, [4, 6, 8])
    ansiedad['alto'] = fuzz.trapmf(ansiedad.universe, [7, 9, 10, 10])

    estres['bajo'] = fuzz.trapmf(estres.universe, [0, 0, 20, 40])
    estres['moderado'] = fuzz.trimf(estres.universe, [30, 50, 70])
    estres['alto'] = fuzz.trapmf(estres.universe, [60, 85, 100, 100])


    reglas = [
        # Reglas de Alto
        ctrl.Rule(sueno['poco'] | ansiedad['alto'] | carga['alta'], estres['alto']),
        
        # Reglas de Moderado
        ctrl.Rule(sueno['adecuado'] | ansiedad['medio'] | carga['media'], estres['moderado']),
        
        # Reglas de Bajo
        ctrl.Rule(sueno['bueno'] & ansiedad['bajo'] & carga['baja'], estres['bajo']),
        
        # REGLA DE SEGURIDAD 
        ctrl.Rule(sueno['adecuado'] & ansiedad['bajo'], estres['bajo']),
        ctrl.Rule(sueno['bueno'] & carga['media'], estres['moderado'])
    ]

    #  Sistema de Control
    sistema_control = ctrl.ControlSystem(reglas)
    simulador = ctrl.ControlSystemSimulation(sistema_control)
    
    # Bisector para estabilidad
    estres.defuzzify_method = 'bisector' 

    # Asignación de inputs
    simulador.input['sueno'] = horas_sueno
    simulador.input['carga'] = num_materias
    simulador.input['ansiedad'] = nivel_ansiedad

    # 5. Computar con manejo de error
    try:
        simulador.compute()
        return simulador.output['estres']
    except Exception:
        
        return 50.0