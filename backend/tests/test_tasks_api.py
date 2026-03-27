from uuid import uuid4

from fastapi.testclient import TestClient

from src.main import app


def test_task_crud_flow() -> None:
    unique_suffix = uuid4().hex[:8]
    title = f"CI Task {unique_suffix}"

    with TestClient(app) as client:
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "ok"

        create_response = client.post(
            "/api/v1/tasks",
            json={
                "title": title,
                "description": "Task created during CI pipeline",
            },
        )
        assert create_response.status_code == 201

        created_task = create_response.json()
        task_id = created_task["id"]

        list_response = client.get("/api/v1/tasks")
        assert list_response.status_code == 200
        assert any(task["id"] == task_id for task in list_response.json())

        update_response = client.put(
            f"/api/v1/tasks/{task_id}",
            json={
                "title": f"{title} Updated",
                "description": "Task updated during CI pipeline",
                "is_done": True,
            },
        )
        assert update_response.status_code == 200
        assert update_response.json()["is_done"] is True

        delete_response = client.delete(f"/api/v1/tasks/{task_id}")
        assert delete_response.status_code == 204

        get_response = client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == 404
