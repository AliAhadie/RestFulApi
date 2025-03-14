import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
from datetime import datetime
from accounts.models import User


@pytest.fixture
def common_user(django_user_model):
    return User.objects.create_user(
        email="testuser@email.com",
        password="Ali@12342002",
    )


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
class TestPostApi:

    def test_get_post(self, api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post(self, common_user, api_client):
        url = reverse("blog:api-v1:post-list")
        user = common_user
        api_client.force_authenticate(user=user)


        data = {

            "title": "Test Post",
            "content": "This is a test post",
            "status": 'true',
            "published_date": datetime.now().isoformat(),
            'category': '1',
        }

        response = api_client.post(url, data)
        print(response.data)
        assert response.status_code == 201
