import pytest
from analysis.models import Corpus, Transcript, UploadFile
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient


@pytest.fixture
def owner(db, django_user_model):
    return django_user_model.objects.create_user(
        username='owner', password='owner-password')


@pytest.fixture
def other_user(db, django_user_model):
    return django_user_model.objects.create_user(
        username='other', password='other-password')


@pytest.fixture
def owner_corpus(db, owner, tarsp_category):
    return Corpus.objects.create(
        user=owner, name='owner_corpus', status='created',
        method_category=tarsp_category)


@pytest.fixture
def other_corpus(db, other_user, tarsp_category):
    return Corpus.objects.create(
        user=other_user, name='other_corpus', status='created',
        method_category=tarsp_category)


@pytest.fixture
def client_for(db):
    def _client(user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client
    return _client


def _upload_data(corpus):
    return {
        'name': 'test.cha',
        'corpus': corpus.pk,
        'status': 'pending',
        'content': SimpleUploadedFile('test.cha', b'*CHI:\thallo .\n'),
    }


def test_upload_file_to_own_corpus(client_for, owner, owner_corpus):
    response = client_for(owner).post(
        '/api/upload_files/', _upload_data(owner_corpus), format='multipart')

    assert response.status_code == 201


def test_upload_file_to_other_corpus_denied(
        client_for, owner_corpus, other_user):
    response = client_for(other_user).post(
        '/api/upload_files/', _upload_data(owner_corpus), format='multipart')

    assert response.status_code == 400
    assert not UploadFile.objects.exists()
    assert not owner_corpus.transcripts.exists()


def test_upload_file_without_corpus_denied(client_for, other_user):
    data = _upload_data(Corpus(pk=1))
    del data['corpus']
    response = client_for(other_user).post(
        '/api/upload_files/', data, format='multipart')

    assert response.status_code == 400
    assert not UploadFile.objects.exists()


def test_upload_file_unauthenticated_denied(db, owner_corpus):
    response = APIClient().post(
        '/api/upload_files/', _upload_data(owner_corpus), format='multipart')

    assert response.status_code in (401, 403)
    assert not UploadFile.objects.exists()
    assert not owner_corpus.transcripts.exists()


def test_upload_file_error_does_not_reveal_corpus_existence(
        client_for, owner_corpus, other_user):
    existing = client_for(other_user).post(
        '/api/upload_files/', _upload_data(owner_corpus), format='multipart')
    missing_data = _upload_data(owner_corpus)
    missing_data['corpus'] = owner_corpus.pk + 1000
    missing = client_for(other_user).post(
        '/api/upload_files/', missing_data, format='multipart')

    assert existing.status_code == missing.status_code == 400
    assert existing.json()['corpus'][0].replace(
        str(owner_corpus.pk), 'X') == missing.json()['corpus'][0].replace(
        str(owner_corpus.pk + 1000), 'X')


def test_create_transcript_in_other_corpus_denied(
        client_for, owner_corpus, other_user):
    response = client_for(other_user).post('/api/transcripts/', {
        'name': 'injected',
        'status': Transcript.CREATED,
        'status_name': 'Created',
        'corpus': owner_corpus.pk,
        'content': SimpleUploadedFile('t.cha', b'*CHI:\thallo .\n'),
    }, format='multipart')

    assert response.status_code == 400
    assert not Transcript.objects.exists()


def test_move_transcript_to_other_corpus_denied(
        client_for, owner, owner_corpus, other_corpus):
    transcript = Transcript.objects.create(
        name='mine', status=Transcript.CREATED, corpus=owner_corpus)
    response = client_for(owner).patch(
        f'/api/transcripts/{transcript.pk}/',
        {'corpus': other_corpus.pk}, format='json')

    assert response.status_code == 400
    transcript.refresh_from_db()
    assert transcript.corpus == owner_corpus


def test_superuser_can_upload_to_any_corpus(
        client_for, admin_user, owner_corpus):
    response = client_for(admin_user).post(
        '/api/upload_files/', _upload_data(owner_corpus), format='multipart')

    assert response.status_code == 201
