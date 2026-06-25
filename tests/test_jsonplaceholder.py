import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    return session


def test_get_post_returns_200(api_session):
    response = api_session.get(f"{BASE_URL}/posts/1", timeout=10)
    assert response.status_code == 200


def test_get_post_has_correct_id(api_session):
    response = api_session.get(f"{BASE_URL}/posts/1", timeout=10)
    data = response.json()
    assert data["id"] == 1


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_post_id_matches(api_session, post_id):
    response = api_session.get(f"{BASE_URL}/posts/{post_id}", timeout=10)
    data = response.json()
    assert data["id"] == post_id


def test_post_has_required_fields(api_session):
    response = api_session.get(f"{BASE_URL}/posts/1", timeout=10)
    data = response.json()
    assert "userId" in data
    assert "id" in data
    assert "title" in data
    assert "body" in data


def test_post_field_types(api_session):
    response = api_session.get(f"{BASE_URL}/posts/1", timeout=10)
    data = response.json()
    assert isinstance(data["userId"], int)
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["body"], str)


def test_get_nonexistent_post_returns_404(api_session):
    response = api_session.get(f"{BASE_URL}/posts/999", timeout=10)
    assert response.status_code == 404


def test_nonexistent_post_returns_empty_body(api_session):
    response = api_session.get(f"{BASE_URL}/posts/999", timeout=10)
    data = response.json()
    assert data == {}