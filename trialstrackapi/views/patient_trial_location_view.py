from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import Patient, TrialLocation, PatientTrialLocation
from trialstrackapi.models.researcher import Researcher
from trialstrackapi.serializers import PatientTrialLocationSerializer


class PatientTrialLocationView(ViewSet):
    def retrieve(self, request, pk):
        try:
            patient_trial_location = PatientTrialLocation.objects.get(pk=pk)
            serializer = PatientTrialLocationSerializer(patient_trial_location)
            return Response(serializer.data)
        except PatientTrialLocation.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        patient_trial_locations = PatientTrialLocation.objects.all()
        trial_location_id = request.query_params.get("trial_location_id", None)
        if trial_location_id is not None:
            patient = patient_trial_locations.filter(
                trial_location_id=trial_location_id
            )
        serializer = PatientTrialLocationSerializer(patient_trial_locations, many=True)
        return Response(serializer.data)

    def create(self, request):
        trial_location = TrialLocation.objects.get(pk=request.data["trial_location_id"])
        patient = Patient.objects.get(pk=request.data["patient_id"])
        researcher = Researcher.objects.get(pk=request.data["researcher_id"])
        patient_trial_location = PatientTrialLocation.objects.create(
            trial_location=trial_location,
            patient=patient,
            researcher=researcher,
            status=request.data["status"],
        )
        serializer = PatientTrialLocationSerializer(patient_trial_location)
        return Response(serializer.data)

    def update(self, request, pk):
        patient_trial_location = PatientTrialLocation.objects.get(pk=pk)
        trial_location = PatientTrialLocation.objects.get(
            pk=request.data["trial_location_id"]
        )
        patient = Patient.objects.get(pk=request.data["patient_id"])
        patient_trial_location.status = request.data["status"]
        patient_trial_location.trial_location = trial_location
        patient_trial_location.patient = patient
        patient_trial_location.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        trial_location_ = PatientTrialLocation.objects.get(pk=pk)
        trial_location_.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
