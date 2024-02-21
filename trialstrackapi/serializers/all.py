from rest_framework import serializers
from trialstrackapi.models import (
    ClinicalTrial,
    Location,
    StudyType,
    ClinicalTrialLocation,
)


class ClinicalTrialLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalTrialLocation
        fields = ("id", "clinical_trial", "location", "status")


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
        fields = ("id", "user", "name", "address", "city", "state", "zip", "country")


class ClinicalTrialsWithStudyTypeSerializer(serializers.ModelSerializer):
    study_type = StudyTypeSerializer()

    class Meta:
        model = ClinicalTrial
        fields = (
            "id",
            "nct_id",
            "title",
            "study_type",
            "overall_status",
            "brief_summary",
            "detail_description",
            "phase",
            "eligibility",
            "study_first_submit_date",
            "last_update_submit_date",
        )
        depth: 2
