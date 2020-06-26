from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView

from .models import Item


class AdminRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, item_id=kwargs["id"])
        return reverse("admin:items_item_change", kwargs={"object_id": item.id})
