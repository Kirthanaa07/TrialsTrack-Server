from datetime import datetime
import json
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod
from rest_framework import serializers, status
from trialstrackapi.models import Trial, User
from trialstrackapi.models.location import Location
from trialstrackapi.models.trial_location import TrialLocation
from trialstrackapi.serializers import (
    TrialSerializer,
)
import requests
from django.http import JsonResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TrialView(ViewSet):
    def retrieve(self, request, pk):
        try:
            trial = Trial.objects.get(pk=pk)
            serializer = TrialSerializer(trial)
            return Response(serializer.data)
        except Trial.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        trials = Trial.objects.all()
        location_id = request.query_params.get("location_id", None)
        # https://stackoverflow.com/questions/48685555/how-to-filter-joined-models-in-django
        if location_id is not None:
            trials = trials.filter(trial_locations__location_id=location_id)
        serializer = TrialSerializer(trials, many=True)
        return Response(serializer.data)

    def create(self, request):
        trial = Trial.objects.create(
            nct_id=request.data["nct_id"],
            title=request.data["title"],
            brief_title=request.data["brief_title"],
            study_type=request.data["study_type"],
            overall_status=request.data["overall_status"],
            brief_summary=request.data["brief_summary"],
            detail_description=request.data["detail_description"],
            phase=request.data["phase"],
            eligibility=request.data["eligibility"],
            study_first_submit_date=request.data["study_first_submit_date"],
            last_update_submit_date=request.data["last_update_submit_date"],
            lead_sponsor_name=request.data["lead_sponsor_name"],
            imported_date=request.data["imported_date"],
        )
        serializer = TrialSerializer(trial)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        trial = Trial.objects.get(pk=pk)
        trial.nct_id = request.data["nct_id"]
        trial.title = request.data["title"]
        trial.brief_title = request.data["brief_title"]
        trial.study_type = request.data["study_type"]
        trial.overall_status = request.data["overall_status"]
        trial.brief_summary = request.data["brief_summary"]
        trial.detail_description = request.data["detail_description"]
        trial.phase = request.data["phase"]
        trial.eligibility = request.data["eligibility"]
        trial.study_first_submit_date = request.data["study_first_submit_date"]
        trial.last_update_submit_date = request.data["last_update_submit_date"]
        trial.lead_sponsor_name = request.data["lead_sponsor_name"]
        trial.save()
        serializer = TrialSerializer(trial)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        trial = Trial.objects.get(pk=pk)
        trial.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=[HTTPMethod.POST], url_path="import", detail=False)
    def import_by_nct_ids(self, request):
        # https://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django
        nct_ids = json.loads(request.body.decode("utf-8"))
        for nct in nct_ids:
            trial = Trial.objects.filter(nct_id=nct)
            if trial.count() != 0:
                continue
            elif trial.count() == 0:
                url = f"https://clinicaltrials.gov/api/v2/studies/{nct}"
                response = requests.get(url, timeout=30)
                data = json.loads(response.content)

                brief_title = ""
                official_title = ""
                study_type = ""
                overall_status = ""
                brief_summary = ""
                detailed_description = ""
                eligibility = ""
                lead_sponsor_name = ""

                if "protocolSection" in data:
                    if "identificationModule" in data["protocolSection"]:
                        if (
                            "briefTitle"
                            in data["protocolSection"]["identificationModule"]
                        ):
                            brief_title = data["protocolSection"][
                                "identificationModule"
                            ]["briefTitle"]
                        if (
                            "officialTitle"
                            in data["protocolSection"]["identificationModule"]
                        ):
                            official_title = data["protocolSection"][
                                "identificationModule"
                            ]["officialTitle"]
                    if "designModule" in data["protocolSection"]:
                        if "studyType" in data["protocolSection"]["designModule"]:
                            study_type = data["protocolSection"]["designModule"][
                                "studyType"
                            ]
                        if "phases" in data["protocolSection"]["designModule"]:
                            phases = data["protocolSection"]["designModule"]["phases"]

                    if "statusModule" in data["protocolSection"]:
                        if "overallStatus" in data["protocolSection"]["statusModule"]:
                            overall_status = data["protocolSection"]["statusModule"][
                                "overallStatus"
                            ]
                        if (
                            "studyFirstSubmitDate"
                            in data["protocolSection"]["statusModule"]
                        ):
                            study_first_submit_date = data["protocolSection"][
                                "statusModule"
                            ]["studyFirstSubmitDate"]

                        if (
                            "lastUpdateSubmitDate"
                            in data["protocolSection"]["statusModule"]
                        ):
                            last_update_submit_date = data["protocolSection"][
                                "statusModule"
                            ]["lastUpdateSubmitDate"]

                    if "descriptionModule" in data["protocolSection"]:
                        if (
                            "briefSummary"
                            in data["protocolSection"]["descriptionModule"]
                        ):
                            brief_summary = data["protocolSection"][
                                "descriptionModule"
                            ]["briefSummary"]

                    if "descriptionModule" in data["protocolSection"]:
                        if (
                            "detailedDescription"
                            in data["protocolSection"]["descriptionModule"]
                        ):
                            detailed_description = data["protocolSection"][
                                "descriptionModule"
                            ]["detailedDescription"]

                    if "eligibilityModule" in data["protocolSection"]:
                        if (
                            "eligibilityCriteria"
                            in data["protocolSection"]["eligibilityModule"]
                        ):
                            eligibility = data["protocolSection"]["eligibilityModule"][
                                "eligibilityCriteria"
                            ]

                    if "sponsorCollaboratorsModule" in data["protocolSection"]:
                        if (
                            "leadSponsor"
                            in data["protocolSection"]["sponsorCollaboratorsModule"]
                        ):
                            lead_sponsor_name = data["protocolSection"][
                                "sponsorCollaboratorsModule"
                            ]["leadSponsor"]["name"]

                new_trial = Trial.objects.create(
                    nct_id=nct,
                    title=official_title,
                    brief_title=brief_title,
                    study_type=study_type,
                    overall_status=overall_status,
                    brief_summary=brief_summary,
                    detail_description=detailed_description,
                    phase=";".join(phases),
                    eligibility=eligibility,
                    study_first_submit_date=study_first_submit_date,
                    last_update_submit_date=last_update_submit_date,
                    lead_sponsor_name=lead_sponsor_name,
                    imported_date=datetime.now(),
                )

                if "protocolSection" in data:
                    if "contactsLocationsModule" in data["protocolSection"]:
                        if (
                            "locations"
                            in data["protocolSection"]["contactsLocationsModule"]
                        ):
                            locations = data["protocolSection"][
                                "contactsLocationsModule"
                            ]["locations"]

                            for location in locations:
                                facility = ""
                                loc_status = ""
                                if "facility" in location:
                                    facility = location["facility"]
                                    if "city" in location:
                                        city = location["city"]
                                    if "state" in location:
                                        state = location["state"]
                                    if "zip" in location:
                                        zip = location["zip"]
                                    if "country" in location:
                                        country = location["country"]
                                    if "geoPoint" in location:
                                        if "lat" in location["geoPoint"]:
                                            lat = location["geoPoint"]["lat"]
                                        if "lon" in location["geoPoint"]:
                                            lon = location["geoPoint"]["lon"]
                                    if "status" in location:
                                        loc_status = location["status"]

                                    contact_name = ""
                                    contact_phone = ""
                                    contact_email = ""
                                    pi_name = ""
                                    if "contacts" in location:
                                        contacts = location["contacts"]
                                        for contact in contacts:
                                            if "role" in contact:
                                                if contact["role"] == "CONTACT":
                                                    if "name" in contact:
                                                        contact_name = contact["name"]
                                                    if "phone" in contact:
                                                        contact_phone = contact["phone"]
                                                    if "email" in contact:
                                                        contact_email = contact["email"]
                                                if (
                                                    contact["role"]
                                                    == "PRINCIPAL_INVESTIGATOR"
                                                ):
                                                    if "name" in contact:
                                                        pi_name = contact["name"]

                                    existingLocation = Location.objects.filter(
                                        name=facility
                                    )
                                    if existingLocation.count() == 0:
                                        new_location = Location.objects.create(
                                            name=facility,
                                            city=city,
                                            state=state,
                                            zip=zip,
                                            country=country,
                                            geo_lat=lat,
                                            geo_lon=lon,
                                            created_date=datetime.now(),
                                        )
                                        TrialLocation.objects.create(
                                            trial=Trial.objects.get(pk=new_trial.id),
                                            location=Location.objects.get(
                                                pk=new_location.id
                                            ),
                                            contact_name=contact_name,
                                            contact_phone=contact_phone,
                                            contact_email=contact_email,
                                            pi_name=pi_name,
                                            status=loc_status,
                                        )
                                    else:
                                        TrialLocation.objects.create(
                                            trial=Trial.objects.get(pk=new_trial.id),
                                            location=Location.objects.get(
                                                pk=existingLocation[0].id
                                            ),
                                            contact_name=contact_name,
                                            contact_phone=contact_phone,
                                            contact_email=contact_email,
                                            pi_name=pi_name,
                                            status=loc_status,
                                        )

        return Response(None, status=status.HTTP_200_OK)
