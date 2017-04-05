from django.contrib.auth.models import User, Group 
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer, SpotSerializer
from spot.models import Spot
from rest_framework import generics

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

