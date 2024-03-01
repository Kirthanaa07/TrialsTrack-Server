from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import Researcher, User, Location
from trialstrackapi.serializers import ResearcherSerializer

class ResearcherView(ViewSet):
  def retrieve(self, request, pk):
    try:
      researcher = Researcher.objects.get(pk=pk)
      serializer = ResearcherSerializer(researcher)
      return Response(serializer.data)
    except Researcher.DoesNotExist as ex:
      return Response({"message":ex.args[0]},status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    researcher = Researcher.objects.all()
    user_id = request.query_params.get("user_id", None)
    if user_id is not None:
        researcher = researcher.filter(user_id=user_id)
    serializer = ResearcherSerializer(researcher, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    user = User.objects.get(pk=request.data["user_id"])
    location = Location.objects.get(pk=request.data["location_id"])
    researcher = Researcher.objects.create(
      department=request.data["department"],
      user=user,
      location=location,
    )
    serializer = ResearcherSerializer(researcher)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    researcher = Researcher.objects.get(pk=pk)
    researcher.department = request.data["department"]
    user = User.objects.get(pk=request.data["user_id"])
    location = Location.objects.get(pk=request.data["location_id"])
    researcher.user = user
    researcher.location = location
    researcher.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def delete(self, request, pk):
    researcher = Researcher.objects.get(pk=pk)
    researcher.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
