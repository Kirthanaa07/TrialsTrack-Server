from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import TrialLocation, Trial, Location
from trialstrackapi.serializers import TrialLocationSerializer


class TrialLocationView(ViewSet):
    def retrieve(self, request, pk):
        try:
            trial_location = TrialLocation.objects.get(pk=pk)
            serializer = TrialLocationSerializer(trial_location)
            return Response(serializer.data)
        except TrialLocation.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        trial_location = TrialLocation.objects.all()
        location = request.query_params.get("location", None)
        if location is not None:
            location = location.filter(location, many=True)
        serializer = TrialLocationSerializer(trial_location, many=True)
        return Response(serializer.data)

    def create(self, request):
        trial = Trial.objects.get(pk=request.data["trial_id"])
        location = Location.objects.get(pk=request.data["location_id"])
        trial_location = TrialLocation.objects.create(
            status=request.data["status"],
            contact_name=request.data["contact_name"],
            contact_phone=request.data["contact_phone"],
            contact_email=request.data["contact_email"],
            pi_name=request.data["pi_name"],
            location=location,
            trial=trial,
        )
        serializer = TrialLocationSerializer(trial_location)
        return Response(serializer.data)

    def update(self, request, pk):
        trial_location = TrialLocation.objects.get(pk=pk)
        trial = Trial.objects.get(pk=request.data["trial_id"])
        location = Location.objects.get(pk=request.data["location_id"])
        trial_location.trial = trial
        trial_location.location = location
        trial_location.status = request.data["status"]
        trial_location.contact_name = request.data["contact_name"]
        trial_location.contact_phone = request.data["contact_phone"]
        trial_location.contact_email = request.data["contact_email"]
        trial_location.pi_name = request.data["pi_name"]
        trial_location.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        trial_location = TrialLocation.objects.get(pk=pk)
        trial_location.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
