from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import Sponsor
from trialstrackapi.serializers import SponsorSerializer

class SponsorView(ViewSet):
  def retrieve(self, request, pk):
    try:
      sponsor = Sponsor.objects.get(pk=pk)
      serializer = SponsorSerializer(sponsor)
      return Response(serializer.data)
    except Sponsor.DoesNotExist as ex:
      return Response({"message":ex.args[0]},status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    sponsor = Sponsor.objects.all()
    serializer = SponsorSerializer(sponsor, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    sponsor = Sponsor.objects.create(
      name=request.data["name"],
    )
    serializer = SponsorSerializer(sponsor)
    return Response(serializer.data)
  
  def update(self, request, pk):
    sponsor = Sponsor.objects.get(pk=pk)
    sponsor.name = request.data["name"]
    sponsor.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def delete(self, request, pk):
    sponsor = Sponsor.objects.get(pk=pk)
    sponsor.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
