from __future__ import unicode_literals
from django.db import models

import pyproj as proj
from shapely import geometry

class Spot(models.Model):
    #Already has an ID equivalent to models.AutoField(primary_key=True)
    lat        = models.DecimalField(max_digits=9, decimal_places=6)
    lon        = models.DecimalField(max_digits=9, decimal_places=6) 
    avail      = models.BooleanField(default=False)
    time_from  = models.FloatField()
    time_to    = models.FloatField()

    def spots_within_radius(origin, radius):
        """ 
        Assume that radius is supplied with its origin, and that they are passed as seperate parameters.
        Assume radius is in meters.
        Assume radius is a list in the form [lon, lat]! Devise a test and a simple way to correct, if possible.
        """
        spots_in_range = []

        # Correct for the curvature of the Earth, assuming WGS84 geographic coordinates (not GoogleMaps projection epsg:900913).
        # (We are abrtacting the geography into geometry, for simplicity.)
        crs_wgs = proj.Proj(init='epsg:4326')
        x, y = proj.transform(crs_wgs, crs_bng, origin[0], origin[1])
 
        #create a coordinate pair for the origin of the radius.
        origin_point = geometry.Point(origin)

        #create a circle, based on the radius and its origin, to measure against.
        search_radius_buffer = origin_point.buffer(radius)
        
        all_spots = Spot.objects.all()
        for spot in all_spots:
            spot_point = [spot.lon, spot.lat]
            if spot_point.within(circle_buffer): 
                spots_in_range.append(spot)

        return spots_in_range

        # Removeing. Avoid reinventing what already exists in libraries:
        #earthRadius = 6371 
        #distanceLat = math.radians(destinationLat-originLat)
        #distanceLon = math.radians(destinationLon-originLon)
        #a = math.sin(distanceLat/2) * math.sin(distanceLat/2) + math.cos(math.radians(originLat)) \
        #    * math.cos(math.radians(destinationLat)) * math.sin(distanceLon/2) * math.sin(distanceLon/2)
        #c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        #return earthRadius * c




        
