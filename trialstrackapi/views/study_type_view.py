# from datetime import datetime
# from django.http import HttpResponseServerError
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from http import HTTPMethod
# from rest_framework import serializers, status
# from trialstrackapi.serializers import StudyTypeSerializer

# class StudyTypeView(ViewSet):
#   def retrieve(self, request, pk):
#     try:
#       study_type = StudyType.objects.get(pk=pk)
#       serializer = StudyTypeSerializer(study_type)
#       return Response(serializer.data)
#     except StudyType.DoesNotExist as ex:
#       return Response({"message":ex.args[0]},status=status.HTTP_404_NOT_FOUND)
    
#   def list(self, request):
#     study_type = StudyType.objects.all()
#     serializer = StudyTypeSerializer(study_type, many=True)
#     return Response(serializer.data)
  
#   def create(self, request):
#     study_type = StudyType.objects.create(
#       name=request.data["name"],
#     )
#     serializer = StudyTypeSerializer(study_type)
#     return Response(serializer.data)
  
#   def update(self, request, pk):
#     study_type = StudyType.objects.get(pk=pk)
#     study_type.name = request.data["name"]
#     study_type.save()
    
#     return Response(None, status=status.HTTP_204_NO_CONTENT)
  
#   def delete(self, request, pk):
#     study_type = StudyType.objects.get(pk=pk)
#     study_type.delete()
#     return Response(None, status=status.HTTP_204_NO_CONTENT)
  
