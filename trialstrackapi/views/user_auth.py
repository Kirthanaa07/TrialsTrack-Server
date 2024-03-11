from http import HTTPMethod
from rest_framework.decorators import api_view
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from trialstrackapi.models import User
from trialstrackapi.models.location import Location
from trialstrackapi.models.patient import Patient
from trialstrackapi.models.researcher import Researcher
from trialstrackapi.serializers import UserWithResearcherPatientSerializer
from rest_framework import status
from rest_framework.decorators import action
import logging

logger = logging.getLogger(__name__)


class UserView(ViewSet):
    def retrieve(self, request, pk):
        try:
            location = User.objects.get(pk=pk)
            serializer = UserWithResearcherPatientSerializer(location)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        users = User.objects.all()
        user_id = request.query_params.get("user_id", None)
        if user_id is not None:
            users = users.filter(user_id=user_id)
        serializer = UserWithResearcherPatientSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        email = request.data["email"]
        existingUser = User.objects.filter(email=email).first()
        if existingUser is not None:
            serializer = UserWithResearcherPatientSerializer(existingUser)
            return Response(serializer.data, status=status.HTTP_200_OK)

        user = User.objects.create(
            uid=request.data["uid"],
            name=request.data["name"],
            email=email,
            role=request.data["role"],
        )
        loc_id = None
        if "location_id" in request.data:
            loc_id = request.data["location_id"]
        department = None
        if "department" in request.data:
            department = request.data["department"]
        age = None
        if "age" in request.data:
            age = request.data["age"]
        gender = None
        if "gender" in request.data:
            gender = request.data["gender"]
        dob = None
        if "dob" in request.data:
            dob = request.data["dob"]
        if loc_id is not None:
            location = Location.objects.get(pk=loc_id)
            Researcher.objects.create(
                user=user, location=location, department=department
            )
        elif age is not None:
            Patient.objects.create(user=user, age=age, gender=gender, dob=dob)
        serializer = UserWithResearcherPatientSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        user.uid = request.data["uid"]
        user.name = request.data["name"]
        user.email = request.data["email"]
        user.role = request.data["role"]
        user.save()

        loc_id = None
        if "location_id" in request.data:
            loc_id = request.data["location_id"]
        department = None
        if "department" in request.data:
            department = request.data["department"]
        age = None
        if "age" in request.data:
            age = request.data["age"]
        gender = None
        if "gender" in request.data:
            gender = request.data["gender"]
        dob = None
        if "dob" in request.data:
            dob = request.data["dob"]
        if loc_id is not None:
            location = Location.objects.get(pk=loc_id)
            researcher = Researcher.objects.filter(user_id=user.id).first()
            if researcher is None:
                Researcher.objects.create(
                    user=user, location=location, department=department
                )
            else:
                researcher.location = location
                researcher.department = department
                researcher.save()

        elif age is not None:
            patient = Patient.objects.filter(user_id=user.id).first()
            if patient is None:
                Patient.objects.create(age=age, gender=gender, dob=dob)
            else:
                patient.age = age
                patient.gender = gender
                patient.dob = dob
                patient.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        researcher = Researcher.objects.filter(user_id=pk).first()
        if researcher is not None:
            researcher.delete()

        patient = Patient.objects.filter(user_id=pk).first()
        if patient is not None:
            patient.delete()

        location = User.objects.get(pk=pk)
        location.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=[HTTPMethod.POST], url_path="check", detail=False)
    def check_user(self, request):
        """Checks to see if User has Associated User Account

        Method arguments:
        request -- The full HTTP request object
        """
        uid = request.data["uid"]
        email = request.data["email"]
        name = request.data["name"]

        # Use the built-in authenticate method to verify
        # authenticate returns the user object or None if no user is found
        user = User.objects.filter(uid=uid).first()

        if user is None:
            # Logged in user does not exist in db with uid. Check by email. IF doesn't exist then add the user as Unassigned user.
            user = User.objects.filter(email=email).first()
            if user is not None:
                # update user uid for existing user.
                user.uid = uid
                user.save()
            else:
                user = User.objects.create(name=name, email=email, role="Unassigned")

        researcher = Researcher.objects.filter(user_id=user.id).first()
        location_id = None
        if researcher is not None:
            location_id = researcher.location_id
        data = {
            "id": user.id,
            "name": user.name,
            "role": user.role,
            "email": user.email,
            "uid": user.uid,
            "location_id": location_id,
        }
        return Response(data)
