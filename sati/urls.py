""" SATI :: URL Configuration """

from baton.autodiscover import admin
from django.urls import path, include
from django.views.generic import TemplateView

from sati.items.views import AdminRedirect
from sati.users.views import EnforcePasswordChangeLoginView

urlpatterns = [
    path("items/<path:id>/", AdminRedirect.as_view()),
    path("admin/login/", EnforcePasswordChangeLoginView.as_view()),
    path("admin/", admin.site.urls),
    path("baton/", include("baton.urls")),
    path("", TemplateView.as_view(template_name="index.html")),
]


from django.conf import settings  # noqa: E402
from django.conf.urls.static import static  # noqa: E402

if settings.DEBUG is True:
    import debug_toolbar  # noqa: E402

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
