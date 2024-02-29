from rest_framework import serializers
from trialstrackapi.models import (
    ClinicalTrial,
    Location,
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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "name", "address", "city", "state", "zip", "country")


class ClinicalTrialLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = ClinicalTrialLocation
        fields = ("id", "location", "status")
