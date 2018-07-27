from django.urls import include, path
from . import views


app_name = 'parking'
urlpatterns = [
    path('add/<zone>/<place_number>/<car_number>/', views.place_add, name='place-add'),
    path('book/<slug:zone>/<int:place_number>/', views.add_booking, name='add-booking'),
    path('zonemap/<int:zone_pk>/', views.get_zone_map, name='place-map'),
    path('entmap/<int:ent_pk>/', views.get_enterprise_map, name='enterprise-map'),
    path('placebookings/<int:zone_pk>/<int:place_number>', views.get_place_bookings, name='place-bookings'),
]
