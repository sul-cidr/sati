from django.contrib.auth import views as auth_views, login as auth_login
from django.http import HttpResponseRedirect


class EnforcePasswordChangeLoginView(auth_views.LoginView):
    template_name = "admin/login.html"

    def form_valid(self, form):
        if form.get_user().require_password_change:
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect("/admin/password_change/")
        else:
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
