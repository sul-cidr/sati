""" SATI :: URL Configuration """

from baton.autodiscover import admin
from django.urls import path, include
from django.views.generic import TemplateView

from sati.users.views import EnforcePasswordChangeLoginView

urlpatterns = [
    path("admin/login/", EnforcePasswordChangeLoginView.as_view()),
    path("admin/", admin.site.urls),
    path("baton/", include("baton.urls")),
    path("", TemplateView.as_view(template_name="index.html")),
]
