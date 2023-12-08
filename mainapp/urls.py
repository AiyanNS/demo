from django.urls import path

from mainapp import views

urlpatterns=[
    path('', views.home, name="Home"),
    path('map', views.interactive_map, name="Map"),
    path('route', views.route, name="Route"),
    path('bicimad_status', views.bicimad_status, name="Bicimad_status"),
    path('bicimad_ui', views.bicimad_ui, name="Bicimad_ui")
]