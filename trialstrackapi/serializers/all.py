from rest_framework import serializers
from trialstrackapi.models import (
    Trial,
    Location,
    TrialLocation,
    Researcher,
    Patient,
    PatientTrialLocation,
    PatientTrialLocationCommunication,
)
from trialstrackapi.models.user import User


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "address",
            "city",
            "state",
            "zip",
            "country",
            "geo_lat",
            "geo_lon",
        )


class ResearcherSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Researcher
        fields = (
            "id",
            "user_id",
            "location_id",
            "location",
            "department",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "uid", "name", "email", "role")


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id",
            "user_id",
            "age",
            "gender",
            "dob",
        )

class PatientWithUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Patient
        fields = (
            "id",
            "user",
            "age",
            "gender",
            "dob",
        )

class PatientWithUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = (
            "id",
            "user",
            "age",
            "gender",
            "dob",
        )


class UserWithResearcherPatientSerializer(serializers.ModelSerializer):
    researcher = ResearcherSerializer()
    patient = PatientSerializer()

    class Meta:
        model = User
        fields = ("id", "uid", "name", "email", "role", "researcher", "patient")


class ResearcherWithUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Researcher
        fields = (
            "id",
            "user",
            "location_id",
            "department",
        )


class LocationWithResearchersSerializer(serializers.ModelSerializer):
    location_researchers = ResearcherWithUserSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "address",
            "city",
            "state",
            "zip",
            "country",
            "location_researchers",
            "geo_lat",
            "geo_lon",
        )


class TrialLocationSerializer(serializers.ModelSerializer):
    location = LocationWithResearchersSerializer()

    class Meta:
        model = TrialLocation
        fields = (
            "id",
            "trial_id",
            "location",
            "contact_name",
            "contact_phone",
            "contact_email",
            "pi_name",
            "status",
        )


class TrialSerializer(serializers.ModelSerializer):
    locations = TrialLocationSerializer(
        many=True, source="trial_locations", read_only=True
    )

    class Meta:
        model = Trial
        fields = (
            "id",
            "nct_id",
            "title",
            "study_type",
            "overall_status",
            "locations",
            "brief_title",
            "brief_summary",
            "detail_description",
            "phase",
            "eligibility",
            "study_first_submit_date",
            "last_update_submit_date",
            "lead_sponsor_name",
        )


class PatientTrialLocationSerializer(serializers.ModelSerializer):
    trial_location = TrialLocationSerializer()
    patient = PatientWithUserSerializer()
    researcher = ResearcherWithUserSerializer()

    class Meta:
        model = PatientTrialLocation
        fields = ("id", "trial_location", "patient", "researcher", "status")


class PatientTrialLocationCommunicationSerializer(serializers.ModelSerializer):
    patient_trial_location = PatientTrialLocationSerializer()

    class Meta:
        model = PatientTrialLocationCommunication
        fields = ("patient_trial_location", "message", "created_by", "created_date")
