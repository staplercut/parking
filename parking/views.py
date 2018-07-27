from . models import Place, Zone, Enterprise
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from django.urls import reverse

states = ('free', 'busy', 'booked',)


@require_http_methods(["GET"])
def place_add(request, zone, place_number, car_number):
    p = Place(zone=Zone.objects.get(letter=zone), place_number=place_number, car_number=car_number)
    p.save()
    places = Place.objects.all()
    data = serializers.serialize('json', places)
    return HttpResponse(data, content_type='application/json')


@require_http_methods(["GET"])
def get_enterprise_map(request, ent_pk):
    current_ent = Enterprise.objects.get(pk=ent_pk)
    zones = Zone.objects.filter(enterprise=current_ent)
    data = serializers.serialize('json', zones)
    return HttpResponse(data, content_type='application/json')


@require_http_methods(["GET"])
def get_zone_map(request, **kwargs):
    current_zone = Zone.objects.get(pk=kwargs['zone_pk'])
    places = Place.objects.filter(Q(state=states.index('busy')) | Q(state=states.index('booked')), zone=current_zone)
    quantity = current_zone.quantity
    dummy = [Place(zone=current_zone, place_number=x) for x in range(1, quantity+1)]
    for place in places:
        n = place.place_number
        dummy[n] = place
    data = {
        'zone name': current_zone.name,
        'zone letter': current_zone.letter,
        'place quantity': current_zone.quantity,
        'default booking duration': Place._meta.get_field('booking_duration').get_default(),
        'places': {x.place_number: {'state': x.state,
                                    'link to bookings': ('http://127.0.0.1:8000' +
                                                         reverse('parking:place-bookings', args=[kwargs['zone_pk'], x.place_number])
                                                         if x.state != 0 else '')} for x in dummy}
    }

    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def get_place_bookings(request, zone_pk, place_number):
    place_bookings = Place.objects.filter(zone=zone_pk, place_number=place_number, completed=False)
    current_zone = Zone.objects.get(pk=zone_pk)
    # data = {'zone letter': current_zone.letter}
    # model_data = model_to_dict(current_place)
    # data.update(model_data)
    data = {
        'zone name': current_zone.name,
        'zone letter': current_zone.letter,
        'place number': place_number,
        'bookings': {str(x.booking_start): model_to_dict(x) for x in place_bookings}
    }
    return JsonResponse(data, safe=False)


# checks if requested booking_start time with requested booking_duration is available
def get_availability(zone_pk, place_number, booking_start, booking_duration):
    # function placeholder
    return True


def get_place_option(booking_start, booking_duration):
    # function placeholder
    # returns place in different zone that user can request for booking
    return True


@require_http_methods(["GET"])
def add_booking(request,  **kwargs):
    zone_pk = kwargs['zone_pk']
    place_number = kwargs['place_number']
    car_number = kwargs['car_number']
    booking_start = kwargs['booking_start']
    booking_duration = kwargs['booking_duration']
    comment = kwargs['comment']
    place_requested = Place(
        zone=zone_pk, place_number=place_number, car_number=car_number, booking_start=booking_start,
        booking_duration=booking_duration, comment=comment)
    # getting a queryset of requested place DB records(bookings) that are not completed
    places = Place.objects.filter(zone=Zone.objects.get(pk=zone_pk), place_number=place_number, completed=False)
    # case of empty queryset means that all bookings for requested place are completed
    if not places:
        place_requested.book()
    # case of queryset containing completed=False objects (ongoing and/or planned booking(s))
    else:
        if get_availability(zone_pk, place_number, booking_start, booking_duration):
            place_requested.book()
        else:
            get_place_option(booking_start, booking_duration)
    return True


@require_http_methods(["GET"])
def edit_booking(request, **kwargs):
    zone_pk = kwargs['zone_pk']
    place_number = kwargs['place_number']
    booking_start = kwargs['booking_start']
    place = Place.objects.get(zone=zone_pk, place_number=place_number, booking_start=booking_start)
    return True






