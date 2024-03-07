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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "uid", "name", "role")


class ResearcherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Researcher
        fields = (
            "id",
            "user",
            "location",
            "department",
        )


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id",
            "user",
            "age",
            "gender",
            "dob",
        )


class TrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trial
        fields = (
            "id",
            "nct_id",
            "title",
            "study_type",
            "overall_status",
            "brief_title",
            "brief_summary",
            "detail_description",
            "phase",
            "eligibility",
            "study_first_submit_date",
            "last_update_submit_date",
            "lead_sponsor_name",
        )


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "name", "address", "city", "state", "zip", "country")


class LocationWithResearchersSerializer(serializers.ModelSerializer):
    location_researchers = ResearcherSerializer(
        many=True, source="location_researchers", read_only=True
    )

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
        )


class TrialLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = TrialLocation
        fields = ("id", "location", "status")


class PatientTrialLocationSerializer(serializers.ModelSerializer):
    trial_location = TrialLocationSerializer()

    class Meta:
        model = PatientTrialLocation
        fields = ("id", "trial_location", "patient", "status")


class PatientTrialLocationCommunicationSerializer(serializers.ModelSerializer):
    patient_trial_location = PatientTrialLocationSerializer()

    class Meta:
        model = PatientTrialLocationCommunication
        fields = ("patient_trial_location", "message", "created_by", "created_date")
