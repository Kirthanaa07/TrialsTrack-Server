from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import Patient, User
from trialstrackapi.serializers import PatientSerializer

class PatientView(ViewSet):
  def retrieve(self, request, pk):
    try:
      patient = Patient.objects.get(pk=pk)
      serializer = PatientSerializer(patient)
      return Response(serializer.data)
    except Patient.DoesNotExist as ex:
      return Response({"message":ex.args[0]},status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    patient = Patient.objects.all()
    trial_location_id = request.query_params.get("trial_location_id", None)
    if trial_location_id is not None:
        patient = patient.filter(trial_location_patients__id=trial_location_id)
    serializer = PatientSerializer(patient, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    user = User.objects.get(pk=request.data["user_id"])
    patient = Patient.objects.create(
      age=request.data["age"],
      gender=request.data["gender"],
      dob=request.data["dob"],
      user=user,
    )
    serializer = PatientSerializer(patient)
    return Response(serializer.data)
  
  def update(self, request, pk):
    patient = Patient.objects.get(pk=pk)
    user = User.objects.get(pk=request.data["user_id"])
    patient.age = request.data["age"]
    patient.gender=request.data["gender"]
    patient.dob=request.data["dob"]
    patient.user=user
    patient.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def delete(self, request, pk):
    patient = Patient.objects.get(pk=pk)
    patient.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
