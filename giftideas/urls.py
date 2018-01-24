"""giftideas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, static
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from app.views import CadeauxListView, CadeauDetailView, IndexView, LoginView, \
    RegisterView
from giftideas import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cadeau/(?P<pk>[-\w]+)/$', CadeauDetailView.as_view(),
        name='produit-detail'),

    url(r'^public/(?P<path>.*)$', static.serve, {
        'document_root': settings.MEDIA_ROOT
    }, name='url_public'),
]

urlpatterns += i18n_patterns(
    url(_(r'^$'), IndexView.as_view(), name="index"),
    url(_(r'gifts'), CadeauxListView.as_view()),
    url(_(r'register'), RegisterView.as_view()),
    url(_(r'login'), LoginView.as_view()),
)