# coding: utf-8
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView


admin.autodiscover()
admin.site.login = staff_member_required(
    admin.site.login, login_url=settings.LOGIN_URL
)

urlpatterns = [
    # https://github.com/stochastic-technologies/django-loginas
    re_path(r'^admin/', include('loginas.urls')),
    # Disable admin login form
    re_path(r'^admin/', admin.site.urls),
    path('', include('kobo.apps.accounts.mfa.urls')),
    path('accounts/', include('allauth.urls')),  # Must be after kpi.url, login
    re_path(
        r'^accounts/register/?',
        RedirectView.as_view(url='/accounts/signup/', permanent=False),
    ),
    re_path(r'^', include('kobo.apps.subsequences.urls')),
    re_path(r'^', include('kpi.urls')),
    re_path(r'^markdownx/', include('markdownx.urls')),
    # re_path(r'^markitup/', include('markitup.urls')),
    re_path(r'^markdownx-uploader/', include('kobo.apps.markdownx_uploader.urls')),
    re_path(r'^help/', include('kobo.apps.help.urls')),
    re_path(
        r'kobocat/',
        RedirectView.as_view(url=settings.KOBOCAT_URL, permanent=True),
    ),
]

if settings.ENABLE_METRICS:
    urlpatterns.append(
        path('', include('django_prometheus.urls')),
    )
