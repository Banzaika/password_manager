import pytest
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from main.views import PasswordCreateRetrieveGetView, PasswordSearchView
from main.models import Password

@pytest.fixture
def create_password_record():
    def _create_password_record(service_name="test_service", password="test_password"):
        # Создание записи в базе данных
        Password.objects.create(service=service_name, password=password)
    return _create_password_record

@pytest.mark.django_db
def test_password_search_view():
    factory = APIRequestFactory()
    view = PasswordSearchView.as_view()

    url = reverse('pass-search') + '?service_name=yundex'
    request = factory.get(url)
    response = view(request)

    assert response.status_code == 200

@pytest.mark.django_db
def test_password_get_view(create_password_record):
    factory = APIRequestFactory()
    view = PasswordCreateRetrieveGetView.as_view()

    create_password_record()

    service_name = "test_service"
    url = reverse('password-get-post', kwargs={'service_name': service_name})
    request = factory.get(url)
    response = view(request, service_name=service_name)

    assert response.status_code == 200

@pytest.mark.django_db
def test_password_create_retrieve_view(create_password_record):
    factory = APIRequestFactory()
    view = PasswordCreateRetrieveGetView.as_view()

    create_password_record()

    service_name = "test_service"
    url = reverse('password-get-post', kwargs={'service_name': service_name})
    data = {
        'password': 'root123'
    }
    request = factory.post(url, data=data)
    response = view(request, service_name=service_name)

    assert response.status_code == 200
    assert 'password' in response.data.keys()
    assert 'service_name' in response.data.keys()