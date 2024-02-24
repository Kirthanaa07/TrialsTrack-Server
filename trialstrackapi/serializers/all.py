from rest_framework import serializers
from trialstrackapi.models import (
    ClinicalTrial,
    Location,
    StudyType,
    ClinicalTrialLocation,
)

class ClinicalTrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalTrial
        fields = (
            "id",
            "nct_id",
            "title",
            "overall_status",
            "brief_summary",
            "detail_description",
            "phase",
            "eligibility",
            "study_first_submit_date",
            "last_update_submit_date",
        )


class StudyTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyType
        fields = ("id", "name")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "name", "address", "city", "state", "zip", "country")


class ClinicalTrialLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = ClinicalTrialLocation
        fields = ("id", "location", "status")

class ClinicalTrialsWithStudyTypeSerializer(serializers.ModelSerializer):
    study_type = StudyTypeSerializer()
    locations = ClinicalTrialLocationSerializer(
        many=True, source="traillocations", read_only=True
    )

    class Meta:
        model = ClinicalTrial
        fields = (
            "id",
            "nct_id",
            "title",
            "study_type",
            "locations",
            "overall_status",
            "brief_summary",
            "detail_description",
            "phase",
            "eligibility",
            "study_first_submit_date",
            "last_update_submit_date",
        )
        depth: 2

