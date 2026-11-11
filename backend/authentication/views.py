from allauth.account.models import EmailConfirmationHMAC
from django.http import HttpResponseRedirect, JsonResponse


def info_from_confirm_key(request, key):
    info = EmailConfirmationHMAC.from_key(key)
    return JsonResponse({'username': info.email_address.user.username,
                         'email': info.email_address.email})


def redirect_confirm(request, key):
    return HttpResponseRedirect('/confirm-email/{}/'.format(key))


def redirect_reset(request, uidb64, token):
    '''Redirects password reset to the frontend'''
    return HttpResponseRedirect('/reset-password/{}/{}/'.format(uidb64, token))


def has_admin_access(request):
    current_user = request.user
    if current_user.is_staff or current_user.is_superuser:
        return JsonResponse({'has_admin_access': True})
    else:
        return JsonResponse({'has_admin_access': False})
