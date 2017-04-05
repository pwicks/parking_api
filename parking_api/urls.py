from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from views import UserViewSet, GroupViewSet, SpotViewSet, RadiusList, ReserveSpot, reservation

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'spots', SpotViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^spots/radius/(?P<radius>.+)/$', RadiusList.as_view()),
    url(r'^spots/reservation/(?P<id>.+)/$', reservation, name='reservation')
]
