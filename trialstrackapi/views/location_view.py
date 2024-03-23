from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import Location, User
from trialstrackapi.serializers import LocationSerializer
from datetime import datetime

class LocationView(ViewSet):
    def retrieve(self, request, pk):
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(location)
            return Response(serializer.data)
        except Location.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def create(self, request):
        location = Location.objects.create(
            name=request.data["name"],
            address=request.data["address"],
            city=request.data["city"],
            state=request.data["state"],
            zip=request.data["zip"],
            country=request.data["country"],
            geo_lat=request.data["geo_lat"],
            geo_lon=request.data["geo_lon"],
            created_date=datetime.now()
        )
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def update(self, request, pk):
        location = Location.objects.get(pk=pk)
        location.name = request.data["name"]
        location.address = request.data["address"]
        location.city = request.data["city"]
        location.state = request.data["state"]
        location.zip = request.data["zip"]
        location.country = request.data["country"],
        location.geo_lat=request.data["geo_lat"],
        location.geo_lon=request.data["geo_lon"],
        location.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        location = Location.objects.get(pk=pk)
        location.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


