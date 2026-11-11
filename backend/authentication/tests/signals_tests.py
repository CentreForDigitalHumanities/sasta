from allauth.account.models import EmailAddress


def test_superuser_email_verified(db, django_user_model):
    admin = django_user_model.objects.create_superuser(
        username='admin', email='admin@example.com', password='admin')

    email = EmailAddress.objects.get(user=admin)
    assert email.email == 'admin@example.com'
    assert email.verified
    assert email.primary


def test_regular_user_email_not_verified(db, django_user_model):
    user = django_user_model.objects.create_user(
        username='user', email='user@example.com', password='user')

    assert not EmailAddress.objects.filter(user=user).exists()
