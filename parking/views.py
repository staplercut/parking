from . models import Place, Zone, Enterprise
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import json
from django.forms.models import model_to_dict

states = ('free', 'busy', 'booked',)


def place_add(request, zone, place_number, car_number):
    if request.method == "GET":
        p = Place(zone=Zone.objects.get(letter=zone), place_number=place_number, car_number=car_number)
        p.save()
        places = Place.objects.all()
        data = serializers.serialize('json', places)
        return HttpResponse(data, content_type='application/json')


def get_enterprise_map(request, ent_pk):
    if request.method == "GET":
        current_ent = Enterprise.objects.get(pk=ent_pk)
        zones = Zone.objects.filter(enterprise=current_ent)
        data = serializers.serialize('json', zones)
        return HttpResponse(data, content_type='application/json')


def get_zone_map(request, zone_pk):
    if request.method == "GET":
        current_zone = Zone.objects.get(pk=zone_pk)
        places = Place.objects.filter(Q(state=states.index('busy')) | Q(state=states.index('booked')), zone=current_zone)
        quantity = current_zone.quantity
        dummy = [Place(zone=current_zone, place_number=x) for x in range(1, quantity+1)]
        for place in places:
            n = place.place_number
            dummy[n] = place
        data = {
            'zone name': current_zone.name,
            'zone letter': current_zone.letter,
            'default booking duration': Place._meta.get_field('booking_duration').get_default(),
            'places': {x.place_number: model_to_dict(x) for x in dummy}
        }
        return JsonResponse(data, safe=False)


def get_place_map(request, zone_pk, place_number):
    if request.method == "GET":
        current_place = Place.objects.get(zone=zone_pk, place_number=place_number, completed=False)
        current_zone = Zone.objects.get(pk=zone_pk)
        data = {'zone letter': current_zone.letter}
        model_data = model_to_dict(current_place)
        data.update(model_data)
        return JsonResponse(data, safe=False)


def place_book(request,  zone, place_number):
    if request.method == "GET":
        p = Place.objects.filter(zone=Zone.objects.get(letter=zone), place_number=place_number).last()
        p.book()
        places = Place.objects.all()
        data = serializers.serialize('json', places)
        return HttpResponse(data, content_type='application/json')




