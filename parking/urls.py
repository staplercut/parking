from django.urls import include, path
from . import views


app_name = 'parking'
urlpatterns = [
    path('add/<zone>/<place_number>/<car_number>/', views.place_add, name='place-add'),
    path('book/<slug:zone>/<int:place_number>/', views.booking, name='booking-book'),
    path('list/<slug:zone>/<int:state>/', views.place_list, name='place-list')
]
