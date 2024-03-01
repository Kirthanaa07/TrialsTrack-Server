from rest_framework import serializers
from trialstrackapi.models import (
    ClinicalTrial,
    Location,
    ClinicalTrialLocation, Sponsor, Researcher, Patient, ClinicalTrialLocationResearcher, PatientClinicalTrialLocation
)

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = (
            "id", "name",
        )
        
class ResearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Researcher
        fields = (
            "id", "user", "location", "department",
        )        

class ClinicalTrialLocationResearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalTrialLocationResearcher
        fields = (
            "id", "clinical_trial_location", "researcher"
        )

class PatientClinicalTrialLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientClinicalTrialLocation
        fields = (
            "id", "clinical_trial_location", "patient", "status"
        )

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id", "user", "age", "gender", "dob",
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
            "sponsor",
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
