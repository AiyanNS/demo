import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler

random.seed(42)
np.random.seed(42)

# Función para calcular el tiempo de retraso
def calcular_tiempo_retraso(nivel_trafico, clima, hora, accidente):
    hora_pico_manana = (7, 9)
    hora_pico_tarde = (13.5, 15.5)
    hora_pico_noche = (19, 20)
    
    if nivel_trafico == 0: # Sin trafico
        retraso_trafico = 0
    elif nivel_trafico == 1: # Trafico congestionado
        retraso_trafico = 5
    elif nivel_trafico == 2: # Todo parado
        retraso_trafico = random.randint(10, 20)
    
    if clima == 0: # Despejado
        retraso_clima = 0 
    elif clima == 1: # Un poco de lluvia
        retraso_clima = 2 
    elif clima == 2: # Inundado/todo hecho mierda
        retraso_clima = 20 
    
    if hora_pico_manana[0] <= hora < hora_pico_manana[1]:
        retraso_pico = 5
    elif hora_pico_tarde[0] <= hora < hora_pico_tarde[1]:
        retraso_pico = 5
    elif hora_pico_noche[0] <= hora < hora_pico_noche[1]:
        retraso_pico = 5
    else:
        retraso_pico = 1
    
    retraso_accidente = 10 if accidente else 0 #si alguien se la pega tarda 10 min mas
    
    return retraso_trafico + retraso_clima + retraso_pico + retraso_accidente

# Función para determinar si es hora punta
def es_hora_punta(fecha):
    hora = fecha.hour
    dia_semana = fecha.weekday()

    # Comprobar si es un día festivo
    if fecha in [datetime(2023, 1, 1), datetime(2023, 12, 25)]:
        return False

    # Consideraciones para días de la semana
    if dia_semana == 0 or dia_semana == 4:  # Lunes o Viernes
        if 7 <= hora < 9 or 13.5 <= hora < 15.5 or 19 <= hora < 20:  # Horas punta
            return True

    # Consideraciones para fines de semana
    if dia_semana >= 5:  # Sábado o Domingo
        return False

    # Resto de los casos
    if 7.5 <= hora < 9.5 or 13 <= hora < 15 or 18.5 <= hora < 20:  # Horas punta
        return True

    return False

# Función para generar el dataframe con información adicional
def generar_dataframe_con_info_adicional(num_muestras=1000):
    # Crear un rango de fechas para el año 2023
    fechas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='20min')

    # Inicializar listas para cada columna
    bus_id = []
    nivel_trafico = []
    clima = []
    accidente = []
    hora_llegada = []
    es_hora_punta_lista = []  # Cambiado el nombre de la lista para evitar conflicto
    dia_del_ano = []
    distancia = []
    es_festivo = []
    dia_de_la_semana = []

    # Iterar sobre el rango de fechas
    for fecha in fechas:
        # Generar datos para cada autobús
        for bus in range(1, 7):
            bus_id.append(bus)
            
            # Condición para evitar tráfico entre las 23:00 y las 7:00
            if 23 <= fecha.hour or fecha.hour < 7:
                nivel_trafico.append(0)
            else:
                nivel_trafico.append(np.random.choice([0, 1, 2], p=[0.6, 0.3, 0.1]))
            
            clima.append(np.random.choice([0, 1, 2], p=[0.95, 0.04, 0.01]))
            accidente.append(random.choices([0, 1], weights=[0.999, 0.001])[0])  # Pequeña probabilidad de accidente
            hora_llegada.append(fecha)
            es_hora_punta_lista.append(es_hora_punta(fecha))
            dia_del_ano.append(fecha.timetuple().tm_yday)
            distancia.append(np.random.uniform(100, 500))
            es_festivo.append(fecha in [datetime(2023, 1, 1), datetime(2023, 12, 25)])
            dia_de_la_semana.append(fecha.weekday())

    # Crear el dataframe
    data = pd.DataFrame({
        'bus_id': bus_id,
        'bus_id': bus_id,
        'nivel_trafico': nivel_trafico,
        'clima': clima,
        'accidente': accidente,
        'hora_llegada': hora_llegada,
        'es_hora_punta': es_hora_punta_lista,  # Cambiado el nombre de la lista para evitar conflicto
        'dia_del_ano': dia_del_ano,
        'distancia': distancia,
        'es_festivo': es_festivo,
        'dia_de_la_semana': dia_de_la_semana
    })

    # Calcular la columna de retraso usando la función
    data['retraso'] = [calcular_tiempo_retraso(row['nivel_trafico'], row['clima'], row['hora_llegada'].hour + row['hora_llegada'].minute/60, row['accidente']) for _, row in data.iterrows()]

    return data

# Generar el dataframe con información adicional
data = generar_dataframe_con_info_adicional()

# Guardar el dataframe en un archivo CSV
data.to_csv('dataframe_con_info_adicional.csv', index=False)

# Imprimir el dataframe
print(data.head())
