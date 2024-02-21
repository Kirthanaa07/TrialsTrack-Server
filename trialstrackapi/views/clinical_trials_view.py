from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import ClinicalTrial, User, StudyType
from trialstrackapi.serializers import ClinicalTrialSerializer,ClinicalTrialsWithStudyTypeSerializer

class ClinicalTrialView(ViewSet):
  def retrieve(self, request, pk):
    try:
      clinical_trial = ClinicalTrial.objects.get(pk=pk)
      serializer = ClinicalTrialsWithStudyTypeSerializer(clinical_trial)
      return Response(serializer.data)
    except ClinicalTrial.DoesNotExist as ex:
      return Response({"message":ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    clinical_trial = ClinicalTrial.objects.all()
    study_type = request.query_params.get('study_type', None)
    if study_type is not None:
      clinical_trial = clinical_trial.filter(study_type_id=study_type)
    serializer = ClinicalTrialsWithStudyTypeSerializer(clinical_trial, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    user = User.objects.get(pk=request.data["user_id"])
    study_type = StudyType.objects.get(pk=request.data["study_type"])
    clinical_trial = ClinicalTrial.objects.create(
      nct_id=request.data["nct_id"],
      title=request.data["title"],
      overall_status=request.data["overall_status"],
      brief_summary=request.data["brief_summary"],
      detail_description=request.data["detail_description"],
      phase=request.data["phase"],
      eligibility=request.data["eligibility"],
      study_first_submit_date=request.data["study_first_submit_date"],
      last_update_submit_date=request.data["last_update_submit_date"],
      user=user,
      study_type=study_type,
    )
    serializer = ClinicalTrialSerializer(clinical_trial)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    clinical_trial = ClinicalTrial.objects.get(pk=pk)
    clinical_trial.nct_id = request.data["nct_id"]
    clinical_trial.title = request.data["title"]
    clinical_trial.overall_status = request.data["overall_status"]
    clinical_trial.brief_summary = request.data["brief_summary"]
    clinical_trial.detail_description = request.data["detail_description"]
    clinical_trial.phase = request.data["phase"]
    clinical_trial.eligibility = request.data["eligibility"]
    clinical_trial.study_first_submit_date = request.data["study_first_submit_date"]
    clinical_trial.last_update_submit_date = request.data["last_update_submit_date"]
    user = User.objects.get(pk=request.data["user_id"])
    study_type = StudyType.objects.get(pk=request.data["study_type"])
    clinical_trial.user = user
    clinical_trial.study_type = study_type
    clinical_trial.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def delete(self, request, pk):
    clinical_trial = ClinicalTrial.objects.get(pk=pk)
    clinical_trial.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
class ClinicalTrialSerializer(serializers.ModelSerializer):
  class Meta:
    model = ClinicalTrial
    fields = ("id", "nct_id", "title", "study_type", "overall_status", "brief_summary", "detail_description", "phase", "eligibility", "study_first_submit_date", "last_update_submit_date")  
  
    