from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
import pandas as pd
import folium
import utm
import json
from .forms import CreateUserForm

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
    return redirect('login')

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
    return render(request,'mainapp/interactivemap.html',context)


def home(request):
    return render(request,'mainapp/home.html')

def interactive_map(request):

    return render(request,'mainapp/interactivemap.html')

def route(request):
    return render(request,'mainapp/route.html')

#@login_required(login_url='login')
def bicimad_ui(request):
    return HttpResponse('bicimadUI')

def bicimad_status(request):
    df=pd.read_csv('madrid.csv',delimiter=',')
    df=df.to_dict(orient='records')
    context={'my_list':json.dumps(df)}
    return render(request,'mainapp/bicimad_map.html',context)


def search_stop(request):
    if request.method=='POST':
        stop_number=request.POST.get('stop_number','')
        return redirect(reverse('stop_detail', kwargs={'stop_number': stop_number}))
    return render(request,'mainapp/search_stop.html')

def stop_detail(request, stop_number):
    dfc = pd.read_csv("./EMT.csv")
    # Reemplazar '6_' en la columna 'IDESTACION' y convertir a numérico
    dfc.loc[:, 'IDESTACION'] = dfc['IDESTACION'].str.replace('6_', '')
    # Obtener coordenadas UTM
    x, y = info_parada(dfc, stop_number)
    if x is not None and y is not None:
        # Convertir de UTM a latitud y longitud
        latitud, longitud = utm.to_latlon(x, y, zone_number=30, northern=True)
        # Crear un mapa centrado en las coordenadas convertidas
        mapa = folium.Map(location=[latitud, longitud], zoom_start=15)
        # Agregar un marcador en las coordenadas
        folium.Marker([latitud, longitud]).add_to(mapa)
        mapa_html = mapa._repr_html_()
        #Información extra sobre la parada
        resultado = datosParada(dfc, stop_number)
        if resultado:
            nombre, lineas, puntAcondicionamiento = resultado
            puntAcondicionamiento = int(puntAcondicionamiento)
            contexto = {
                'stop_number': stop_number,
                'mapa_html': mapa_html,
                'nombre': nombre,
                'lineas': lineas,
                'puntAcondicionamiento': puntAcondicionamiento,
                'color_puntuacion': color_puntuacion(puntAcondicionamiento),  
            }
            return render(request, 'mainapp/infoparada.html', contexto)
        else: 
            mensaje_error = f"No se encontró información para la parada con ID {stop_number}."
            return render(request, 'error.html', {'mensaje_error': mensaje_error})
        # Renderizar la plantilla con la información y el mapa
    else:
       mensaje_error = f"No se encontró información para la parada con ID {stop_number}."
       return render(request, 'error.html', {'mensaje_error': mensaje_error})

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