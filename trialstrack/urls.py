"""trialstrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from trialstrackapi.views import LocationView, TrialView, TrialLocationView, UserView, ResearcherView, PatientView, PatientTrialLocationView, PatientTrialLocationCommunicationView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", UserView, "users")
router.register(r"locations", LocationView, "location")
router.register(r"trials", TrialView, "trial")
router.register(r"trial_locations", TrialLocationView, "trial_location")
router.register(r"researchers", ResearcherView, "researcher")
router.register(r"patients", PatientView, "patient")
router.register(r"patient_trial_locations", PatientTrialLocationView, "patient_trial_location")
router.register(r"patient_trial_location_communications", PatientTrialLocationCommunicationView, "patient_trial_location_communication")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
