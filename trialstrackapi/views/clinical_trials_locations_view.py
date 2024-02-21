from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import ClinicalTrialLocation, ClinicalTrial, Location
from trialstrackapi.serializers import ClinicalTrialLocationSerializer


class ClinicalTrialLocationView(ViewSet):
    def retrieve(self, request, pk):
        try:
            clinical_trial_location = ClinicalTrialLocation.get(pk=pk)
            serializer = ClinicalTrialLocationSerializer(clinical_trial_location)
            return Response(serializer.data)
        except ClinicalTrialLocation.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        clinical_trial_location = ClinicalTrialLocation.objects.all()
        serializer = ClinicalTrialLocationSerializer(clinical_trial_location, many=True)
        return Response(serializer.data)

    def create(self, request):
        clinical_trial = ClinicalTrial.objects.get(pk=request.data["clinical_trial"])
        location = Location.objects.get(pk=request.data["location"])
        clinical_trial_location = ClinicalTrialLocation.objects.create(
            status=request.data["status"],
            location=location,
            clinical_trial=clinical_trial,
        )
        serializer = ClinicalTrialLocationSerializer(clinical_trial_location)
        return Response(serializer.data)

    def update(self, request, pk):
        clinical_trial_location = ClinicalTrialLocation.objects.get(pk=pk)
        clinical_trial = ClinicalTrial.objects.get(pk=request.data["clinical_trial"])
        location = Location.objects.get(pk=request.data["location"])
        clinical_trial_location.clinical_trial = clinical_trial
        clinical_trial_location.location = location
        clinical_trial_location.status = request.data["status"]
        clinical_trial_location.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        clinical_trial_location = ClinicalTrialLocation.objects.get(pk=pk)
        clinical_trial_location.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
