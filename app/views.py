from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, DetailView

from app.forms.login import LoginForm
from app.models import Produit


class CadeauxView(generic.TemplateView):
    template_name = 'cadeaux.html'


class CadeauxListView(LoginRequiredMixin, ListView):
    template_name = 'produit_list.html'
    model = Produit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CadeauDetailView(DetailView):
    template_name = 'produit_detail.html'
    model = Produit


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class LoginView(generic.FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # form.cleaned_data['username']
        username = form.cleaned_data.get('username')
        # if 'a' not in username:
        #     form.add_error('username',
        #                    'Username doit avoir un a')
        #     return super(LoginView, self).form_invalid(form)

        password = form.cleaned_data.get('password')
        if len(password) < 8:
            form.add_error('password',
                           'Minimal length = 8')
            return super(LoginView, self).form_invalid(form)

        user = authenticate(username=username,
                            password=password)
        if user is None:
            form.add_error(None,
                           'Erreur de connexion '
                           '(identifiant ou mot de passe incorrect)')
            return super(LoginView, self).form_invalid(form)

        login(self.request, user)
        # {% if user.is_authenticated %}
        return super(LoginView, self).form_valid(form)