from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Create your views here.
import xgboost as xgb
import pandas as pd
import numpy as np
import joblib
import folium
import utm
import json
from .forms import CreateUserForm
from .models import savedStops, savedBICIMAD, Estacion, BicimadStation
from folium.plugins import MarkerCluster

def login_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
    context={}
    return render(request,'mainapp/login.html',context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register(request):
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+ user)
            return redirect('login')
    context = {'form':form}
    return render(request,'mainapp/register.html',context)

def home(request):
    return render(request,'mainapp/home.html')

def busmap(request):
    dfc = pd.read_csv("./EMT.csv")
    # Reemplazar '6_' en la columna 'IDESTACION' y convertir a numérico
    dfc['IDESTACION'] = dfc['IDESTACION'].str.replace('6_', '').astype(int)
    # Usar la función ver_coordenadas para obtener las coordenadas
    coordenadas = ver_coordenadas(dfc)
    # Inicializar el mapa y el MarkerCluster
    mapa = folium.Map(location=[40.416775, -3.703790], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(mapa)
    # Agregar marcadores al MarkerCluster
    for coord in coordenadas:
        folium.Marker(location=coord).add_to(marker_cluster)
    # Generar el HTML para el mapa
    mapa_html = mapa._repr_html_()
    contexto = {'mapa_html': mapa_html}
    return render(request, 'mainapp/interactivemap.html', contexto)

def route(request):
    return render(request,'mainapp/route.html')

#USER PAGES
@login_required
def favourite(request):
    if request.user.is_authenticated:
        paradas_guardadas = savedStops.objects.filter(user=request.user)
        estaciones_bicimad = savedBICIMAD.objects.filter(user=request.user)
        context = {'paradas_guardadas': paradas_guardadas, 'estaciones_bicimad': estaciones_bicimad}
        return render(request, 'mainapp/favourite.html', context)
    else:
        context = 'No tiene paradas guardadas'
        return render(request, 'mainapp/error.html', context)

def bicimad_ui(request):
    return HttpResponse('bicimadUI')

def bicimad_status(request):
    df = pd.read_csv('madrid.csv', delimiter=',')
    df = df.to_dict(orient='records')
    context = {'my_list': json.dumps(df)}
    return render(request, 'mainapp/bicimad_map.html', context)

def save_station(request, estacion_id):
    # Obtén la estación de Bicimad que se va a guardar
    bicimad_station = get_object_or_404(BicimadStation, id=estacion_id)
    
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        # Verifica si la estación ya está guardada para el usuario
        if not savedBICIMAD.objects.filter(user=request.user, savedStation=bicimad_station).exists():
            # Guarda la estación para el usuario actual
            saved_station = savedBICIMAD(user=request.user, savedStation=bicimad_station)
            saved_station.save()
            messages.success(request, 'Estación guardada correctamente.')
        else:
            messages.warning(request, 'Esta estación ya está en tus favoritos.')
    
    # Redirige directamente a la página del mapa de Bicimad
    return redirect('bicimad_status')


def search_stop(request):
    if request.method=='POST':
        stop_number=request.POST.get('stop_number','')
        return redirect(reverse('stop_detail', kwargs={'stop_number': stop_number}))
    return render(request,'mainapp/search_stop.html')

def stop_detail(request, stop_number):
    stop_number
    station=Estacion.objects.get(IDESTACION=stop_number)
    latitud=station.latitude
    longitud=station.longitude
    if station is not None:
        # Crear un mapa centrado en las coordenadas convertidas
        mapa = folium.Map(location=[latitud, longitud], zoom_start=15)
        # Agregar un marcador en las coordenadas
        folium.Marker([latitud, longitud]).add_to(mapa)
        mapa_html = mapa._repr_html_()
        #Información extra sobre la parada
        nombre = station.DENOMINACION
        lineas = station.LINEAS
        puntAcondicionamiento=station.ACONDICIONAMIENTOVIAJEROS
        puntAcondicionamiento = int(puntAcondicionamiento)
        parada_guardada = savedStops.objects.filter(user=request.user, savedStop_id=stop_number).exists()
        traffic,climate,accident,rush_hour,doy,dist,holliday,dow = 1,0,0,False,100,200,False,3
        result = get_prediction(traffic, climate, accident, rush_hour, doy, dist, holliday, dow)
        contexto = {
            'stop_number': stop_number,
            'mapa_html': mapa_html,
            'nombre': nombre,
            'lineas': lineas,
            'puntAcondicionamiento': puntAcondicionamiento,
            'color_puntuacion': color_puntuacion(puntAcondicionamiento),
            'parada_guardada': parada_guardada,
            'delay':result
        }
                # Verificar si el usuario está autenticado antes de mostrar el botón de guardar
        if request.user.is_authenticated:
            saved_stop, created = savedStops.objects.get_or_create(
                user=request.user,
                savedStop_id=stop_number,
            )
            if not created:
                messages.warning(request, 'Esta parada ya está en tus favoritos.')
            contexto['saved_stop'] = saved_stop
        return render(request, 'mainapp/infoparada.html', contexto)
    else:
       mensaje_error = f"No se encontró información para la parada con ID {stop_number}."
       return render(request, 'mainapp/error.html', {'mensaje_error': mensaje_error})

# Other functions
def datosParada(dfl, idParada):
    if idParada in dfl['IDESTACION'].values:
        # Filtrar el DataFrame para obtener la fila correspondiente al ID de la parada
        informacion_parada = dfl[dfl['IDESTACION'] == idParada]
        nombre = informacion_parada['DENOMINACION'].values[0]
        lineas = informacion_parada['LINEAS'].values[0]
        dfl_copy = dfl.copy()
        dfl_copy['ACONDICIONAMIENTOVIAJEROS'] = dfl_copy['ACONDICIONAMIENTOVIAJEROS'].astype(int)
        puntAcondicionamiento = informacion_parada['ACONDICIONAMIENTOVIAJEROS'].values[0]
        return nombre, lineas, puntAcondicionamiento
    else:return None
    
def info_parada(dfl, stop_number):
    if stop_number in dfl['IDESTACION'].values:
        informacion_parada = dfl[dfl['IDESTACION'] == stop_number]
        x,y = informacion_parada['X'].values[0],informacion_parada['Y'].values[0]
        return x, y
    else:return None

def color_puntuacion(puntuacion):
    if puntuacion >= 4:return "high-score"
    elif puntuacion >= 2:return "medium-score"
    else:return "low-score"

def ver_coordenadas(dfc):
    # Obtener coordenadas UTM para todas las paradas
    coordenadas = []
    for _, row in dfc.iterrows():
        x, y = row['X'], row['Y']
        if pd.notna(x) and pd.notna(y):  # Asegurarse de que las coordenadas no sean NaN
            # Convertir de UTM a latitud y longitud
            latitud, longitud = utm.to_latlon(x, y, zone_number=30, northern=True)
            coordenadas.append((latitud, longitud))
    return coordenadas

def get_prediction(traffic, climate, accident, rush_hour, doy, dist, holliday, dow):
    model_filename = 'modelo_prediccion/xgboost_model.joblib'
    loaded_model = joblib.load(model_filename)
    sample_input_params = np.array([[traffic, climate, accident, rush_hour, doy, dist, holliday, dow]])
    prediction = loaded_model.predict(sample_input_params)
    prediction=prediction[0]*60
    minutes,seconds = round(prediction // 60),round(prediction % 60)
    result=f'Retraso esperado de {minutes}min y {seconds}s aproximadamente. '
    return result
