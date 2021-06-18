from django.urls import path

from app.views import index, bus_stations, pagi_view


urlpatterns = [
    path('', index, name='index'),
    path('bus_stations/', bus_stations, name='bus_stations'),
    path('pagi_stations/', pagi_view, name='pagi_stations')
]
