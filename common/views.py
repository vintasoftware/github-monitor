from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class LoginView(generic.TemplateView):
    template_name = "common/login.html"


class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "common/index.html"
