from django.urls import include, path

from .views import info_from_confirm_key, has_admin_access, redirect_reset

urlpatterns = [
    path('infofromkey/<key>/', info_from_confirm_key),
    path('', include('rest_auth.urls')),
    # password reset
    path('password-reset/<uidb64>/<token>/',
         redirect_reset, name='password_reset_confirm'),
    path('registration/', include('rest_auth.registration.urls')),
    path('has_admin_access/', has_admin_access),
]
