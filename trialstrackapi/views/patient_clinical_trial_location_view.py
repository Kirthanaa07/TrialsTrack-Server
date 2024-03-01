from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import Patient, ClinicalTrialLocation, PatientClinicalTrialLocation
from trialstrackapi.serializers import PatientClinicalTrialLocationSerializer


class PatientClinicalTrialLocationView(ViewSet):
    def retrieve(self, request, pk):
        try:
          patient_clinical_trial_location_ = PatientClinicalTrialLocation.objects.get(pk=pk)
          serializer = PatientClinicalTrialLocationSerializer(patient_clinical_trial_location_)
          return Response(serializer.data)
        except PatientClinicalTrialLocation.DoesNotExist as ex:
          return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        patient_clinical_trial_location_ = PatientClinicalTrialLocation.objects.all()
        serializer = PatientClinicalTrialLocationSerializer(patient_clinical_trial_location_, many=True)
        return Response(serializer.data)

    def create(self, request):
      clinical_trial_location = PatientClinicalTrialLocation.objects.get(pk=request.data["clinical_trial_location_id"])
      patient = Patient.objects.get(pk=request.data["patient_id"])
      patient_clinical_trial_location_ = PatientClinicalTrialLocation.objects.create(
          clinical_trial_location = clinical_trial_location,
          patient = patient,
          status = request.data["status"],
      )
      serializer = PatientClinicalTrialLocationSerializer(patient_clinical_trial_location_)
      return Response(serializer.data)

    def update(self, request, pk):
        patient_clinical_trial_location = PatientClinicalTrialLocation.objects.get(pk=pk)
        clinical_trial_location = PatientClinicalTrialLocation.objects.get(pk=request.data["clinical_trial_location_id"])
        patient = Patient.objects.get(pk=request.data["patient_id"])
        patient_clinical_trial_location.status = request.data["status"]
        patient_clinical_trial_location.clinical_trial_location = clinical_trial_location
        patient_clinical_trial_location.patient = patient
        patient_clinical_trial_location.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        clinical_trial_location_ = PatientClinicalTrialLocation.objects.get(pk=pk)
        clinical_trial_location_.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
