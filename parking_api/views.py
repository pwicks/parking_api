from django.contrib.auth.models import User, Group 
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer, SpotSerializer
from spot.models import Spot
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import json
import time

# This is simply a fixture that stands-in for a user property for origin of radius.
RADIUS_ORIGIN = [-122.463966, 37.803590]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SpotViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Spots to be viewed or edited.
    """
    #queryset = Spot.objects.all()
    queryset = Spot.objects.filter(avail=True)
    serializer_class = SpotSerializer

class RadiusList(generics.ListAPIView):
    serializer_class = SpotSerializer

    def get_queryset(self):
        radius = int(self.kwargs['radius'])

        ids_in_range = []
        avail_spots = Spot.objects.filter(avail=True)
        for spot in avail_spots:
            if spot.withinRadius(RADIUS_ORIGIN, radius):
                ids_in_range.append(spot.id)

        queryset = Spot.objects.filter(pk__in=ids_in_range)

        return queryset

class ReserveSpot(generics.UpdateAPIView):
    # Class based examples hide important details, so I'm going to use a simpler mechanism, below.
    serializer_class = SpotSerializer

    def update(self, request, *args, **kwargs):
        spot_id = self.kwargs(['id'])
        instance = Spot.objects.filter(id=spot_id)
        #instance = self.get_object()
        instance.avail = False
        instance.save()

        serializer = self.get_serializer(instance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

@csrf_exempt
def reservation(request, id):
    """
    Retrieve, update or delete a reservation.
    """
    try:
        print("Request: {0}".format(request))
        print("Request payload: {0}".format(dir(request)))
        print("ID: {0}".format(id))
        spot = Spot.objects.get(id=id)
    except Spot.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        serializer = SpotSerializer(spot, context=serializer_context)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        #data = JSONParser().parse(request)
        #data = request.query_params
        serializer_context = {
            'request': request,
        }
        spot.avail = False
        epoch_time = int(time.time())
        spot.time_from = epoch_time
        data = {
            "lat": spot.lat,
            "lon": spot.lon,
            "time_from": epoch_time + 3600,
            "time_to" : epoch_time,
            "avail": False
        }
        
        serializer = SpotSerializer(spot, data=data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        # This is an abuse of the RESTful nature of the API, but is useful for the moment. 
        # @TODO Replace or remove this.
        spot.available = True
        serializer_context = {
            'request': request,
        }
        serializer = SpotSerializer(spot, context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
