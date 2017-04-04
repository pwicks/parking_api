from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer, SpotSerializer
from spot.models import Spot
from rest_framework import generics

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

