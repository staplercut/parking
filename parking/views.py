from . models import Place, Zone
from django.core import serializers
from django.http import HttpResponse


# place_states = ('free', '', '')


def place_add(request, zone, place_number, car_number):
    if request.method == "GET":
        p = Place(zone=Zone.objects.get(letter=zone), place_number=place_number, car_number=car_number)
        p.save()
        places = Place.objects.all()
        data = serializers.serialize('json', places)
        return HttpResponse(data, content_type='application/json')


def place_list(request, zone, state):
    if request.method == "GET":
        if zone == 'ALL':
            zones = Zone.objects.all()
            p = Place.objects.none()
            for z in zones:
                p = p | Place.objects.filter(zone=z.pk, state=state).last()
        else:
            p = Place.objects.filter(zone=Zone.objects.get(letter=zone))
        data = serializers.serialize('json', p)
        return HttpResponse(data, content_type='application/json')


def booking(request,  zone, place_number):
    if request.method == "GET":
        p = Place.objects.filter(zone=Zone.objects.get(letter=zone), place_number=place_number).last()
        p.book()
        places = Place.objects.all()
        data = serializers.serialize('json', places)
        return HttpResponse(data, content_type='application/json')


