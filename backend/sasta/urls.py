"""sasta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path(r'^blog/', include('blog.urls'))
"""
from analysis import urls as analysis_urls
from analysis import views as analysis_views
from parse import urls as parse_urls
from authentication.views import redirect_confirm
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework import routers

from .index import index
from .proxy_frontend import proxy_frontend


def trigger_error(request):
    '''For testing sentry'''
    division_by_zero = 1 / 0
    return division_by_zero


api_router = routers.DefaultRouter()  # register viewsets with this router
api_router.register(r'upload_files', analysis_views.UploadFileViewSet)
api_router.register(r'transcripts', analysis_views.TranscriptViewSet)
api_router.register(r'corpora', analysis_views.CorpusViewSet)
api_router.register(r'assessment_methods',
                    analysis_views.AssessmentMethodViewSet)
api_router.register(r'method_categories', analysis_views.MethodCategoryViewSet)

if settings.PROXY_FRONTEND:
    spa_url = re_path(r'^(?P<path>.*)$', proxy_frontend)
else:
    spa_url = re_path(r'', index)

urlpatterns = [
    path('admin', RedirectView.as_view(url='/admin/', permanent=True)),
    path('api', RedirectView.as_view(url='/api/', permanent=True)),
    path('api-auth', RedirectView.as_view(url='/api-auth/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('api/analysis/', include(analysis_urls)),
    path('api/parse/', include(parse_urls)),
    path('api/sentry-debug/', trigger_error),
    path('api-auth/', include(
        'rest_framework.urls',
        namespace='rest_framework',
    )),
    path('rest-auth/', include('authentication.urls')),
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
            redirect_confirm, name='account_confirm_email'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns.append(spa_url)  # catch-all; unknown paths to be handled by a SPA
