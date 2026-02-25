import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def calcular_nivel_estres(horas_sueno, num_materias, nivel_ansiedad):
    # 1. Definición de Variables
    sueno = ctrl.Antecedent(np.arange(0, 13, 1), 'sueno')
    carga = ctrl.Antecedent(np.arange(1, 11, 1), 'carga')
    ansiedad = ctrl.Antecedent(np.arange(0, 11, 1), 'ansiedad')
    estres = ctrl.Consequent(np.arange(0, 101, 1), 'estres')

    # 2. Funciones de Pertenencia (Rangos)
    sueno['poco'] = fuzz.trimf(sueno.universe, [0, 0, 6])
    sueno['adecuado'] = fuzz.trimf(sueno.universe, [4, 7, 9])
    sueno['bueno'] = fuzz.trimf(sueno.universe, [8, 12, 12])

    carga['baja'] = fuzz.trimf(carga.universe, [1, 1, 4])
    carga['media'] = fuzz.trimf(carga.universe, [3, 5, 7])
    carga['alta'] = fuzz.trimf(carga.universe, [6, 10, 10])

    ansiedad['bajo'] = fuzz.trimf(ansiedad.universe, [0, 0, 5])
    ansiedad['medio'] = fuzz.trimf(ansiedad.universe, [3, 5, 7])
    ansiedad['alto'] = fuzz.trimf(ansiedad.universe, [6, 10, 10])

    estres['bajo'] = fuzz.trimf(estres.universe, [0, 0, 40])
    estres['moderado'] = fuzz.trimf(estres.universe, [30, 50, 70])
    estres['alto'] = fuzz.trimf(estres.universe, [60, 100, 100])

    # 3. Reglas Lógicas
    regla1 = ctrl.Rule(sueno['poco'] | ansiedad['alto'], estres['alto'])
    regla2 = ctrl.Rule(carga['alta'] & ansiedad['medio'], estres['alto'])
    regla3 = ctrl.Rule(sueno['adecuado'] & carga['media'], estres['moderado'])
    regla4 = ctrl.Rule(sueno['bueno'] & carga['baja'] & ansiedad['bajo'], estres['bajo'])

    # 4. Sistema de Control
    sistema_control = ctrl.ControlSystem([regla1, regla2, regla3, regla4])
    simulador = ctrl.ControlSystemSimulation(sistema_control)

    # Entradas de la función
    simulador.input['sueno'] = horas_sueno
    simulador.input['carga'] = num_materias
    simulador.input['ansiedad'] = nivel_ansiedad

    simulador.compute()
    
    return simulador.output['estres']