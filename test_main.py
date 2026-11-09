import pytest
from fastapi.testclient import TestClient

import database
from main import app


@pytest.fixture(autouse=True)
def temporary_database(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        tmp_path / "test_tasks.db",
    )


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_empty_task_title_rejected():
    with TestClient(app) as client:
        response = client.post(
            "/tasks",
            json={"title": "", "completed": False},
        )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]


def test_create_and_get_task():
    with TestClient(app) as client:
        created = client.post(
            "/tasks",
            json={"title": "Practise automated testing"},
        )

        assert created.status_code == 201
        task = created.json()
        assert task["title"] == "Practise automated testing"
        assert task["completed"] is False

        retrieved = client.get(f"/tasks/{task['id']}")

        assert retrieved.status_code == 200
        assert retrieved.json() == task


def test_complete_task():
    with TestClient(app) as client:
        created = client.post(
            "/tasks",
            json={"title": "Test task completion"},
        )

        assert created.status_code == 201
        task_id = created.json()["id"]

        updated = client.patch(f"/tasks/{task_id}/complete")

        assert updated.status_code == 200
        assert updated.json()["completed"] is True

        retrieved = client.get(f"/tasks/{task_id}")

        assert retrieved.status_code == 200
        assert retrieved.json()["completed"] is True