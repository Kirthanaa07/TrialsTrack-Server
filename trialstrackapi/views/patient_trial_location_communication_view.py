from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import Patient, PatientTrialLocationCommunication
from trialstrackapi.serializers import PatientTrialLocationSerializer
from trialstrackapi.serializers.all import PatientTrialLocationCommunicationSerializer


class PatientTrialLocationCommunicationView(ViewSet):
    def retrieve(self, request, pk):
        try:
            patient_trial_location_communication = (
                PatientTrialLocationCommunication.objects.get(pk=pk)
            )
            serializer = PatientTrialLocationCommunicationSerializer(
                patient_trial_location_communication
            )
            return Response(serializer.data)
        except PatientTrialLocationCommunication.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        patient_trial_location_communication = (
            PatientTrialLocationCommunication.objects.all()
        )
        serializer = PatientTrialLocationCommunicationSerializer(
            patient_trial_location_communication, many=True
        )
        return Response(serializer.data)

    def create(self, request):
        patient_trial_location = PatientTrialLocationCommunication.objects.get(
            pk=request.data["patient_trial_location_id"]
        )
        message = request.data["message"]
        created_by = request.data["created_by"]
        created_date = request.data["created_date"]
        patient_trial_location_communication = (
            PatientTrialLocationCommunication.objects.create(
                patient_trial_location=patient_trial_location,
                message=message,
                created_by=created_by,
                created_date=created_date,
            )
        )
        serializer = PatientTrialLocationCommunicationSerializer(
            patient_trial_location_communication
        )
        return Response(serializer.data)

    def update(self, request, pk):
        patient_trial_location_communication = (
            PatientTrialLocationCommunication.objects.get(pk=pk)
        )
        patient_trial_location = PatientTrialLocationCommunication.objects.get(
            pk=request.data["patient_trial_location_id"]
        )

        patient_trial_location_communication.patient_trial_location = (
            patient_trial_location
        )
        patient_trial_location_communication.message = request.data["message"]
        patient_trial_location_communication.created_by = request.data["created_by"]
        patient_trial_location_communication.created_date = request.data["created_date"]
        patient_trial_location_communication.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        trial_location_ = PatientTrialLocationCommunication.objects.get(pk=pk)
        trial_location_.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
