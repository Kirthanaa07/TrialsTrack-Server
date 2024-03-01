from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import ClinicalTrialLocationResearcher, Researcher, ClinicalTrialLocation
from trialstrackapi.serializers import ClinicalTrialLocationResearcherSerializer


class ClinicalTrialLocationResearcherView(ViewSet):
    def retrieve(self, request, pk):
        try:
          clinical_trial_location_researcher = ClinicalTrialLocationResearcher.objects.get(pk=pk)
          serializer = ClinicalTrialLocationResearcherSerializer(clinical_trial_location_researcher)
          return Response(serializer.data)
        except ClinicalTrialLocationResearcher.DoesNotExist as ex:
          return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        clinical_trial_location_researcher = ClinicalTrialLocationResearcher.objects.all()
        serializer = ClinicalTrialLocationResearcherSerializer(clinical_trial_location_researcher, many=True)
        return Response(serializer.data)

    def create(self, request):
      clinical_trial_location = ClinicalTrialLocation.objects.get(pk=request.data["clinical_trial_location_id"])
      researcher = Researcher.objects.get(pk=request.data["researcher_id"])
      clinical_trial_location_researcher = ClinicalTrialLocationResearcher.objects.create(
          clinical_trial_location = clinical_trial_location,
          researcher = researcher,
      )
      serializer = ClinicalTrialLocationResearcherSerializer(clinical_trial_location_researcher)
      return Response(serializer.data)

    def update(self, request, pk):
        clinical_trial_location_researcher = ClinicalTrialLocationResearcher.objects.get(pk=pk)
        clinical_trial_location = ClinicalTrialLocation.objects.get(pk=request.data["clinical_trial_location_id"])
        researcher = Researcher.objects.get(pk=request.data["researcher_id"])
        clinical_trial_location_researcher.clinical_trial_location = clinical_trial_location
        clinical_trial_location_researcher.researcher = researcher
        clinical_trial_location_researcher.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        clinical_trial_location_researcher = ClinicalTrialLocationResearcher.objects.get(pk=pk)
        clinical_trial_location_researcher.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
