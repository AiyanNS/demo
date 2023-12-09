from django.urls import path

from mainapp import views

urlpatterns=[
    path('', views.home, name="home"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_user,name="logout"),
    path('map', views.interactive_map, name="map"),
    path('route', views.route, name="route"),
    path('search_stop', views.search_stop, name="stop"),
    path('<str:stop_number>', views.stop_detail, name='stop_detail'),
    path('bicimad_status', views.bicimad_status, name="bicimad_status"),
    path('bicimad_ui', views.bicimad_ui, name="bicimad_ui")
]