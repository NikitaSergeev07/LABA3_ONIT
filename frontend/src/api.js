const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
const TASKS_PATH = "/api/v1/tasks";

function normalizeTask(payload) {
  return {
    id: payload.id,
    title: payload.title,
    description: payload.description ?? "",
    isDone: payload.is_done,
    createdAt: payload.created_at,
  };
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = "Unexpected API error";
    try {
      const data = await response.json();
      message = data.detail ?? message;
    } catch {
      message = response.statusText || message;
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export async function listTasks() {
  const data = await request(TASKS_PATH);
  return data.map(normalizeTask);
}

export async function createTask(input) {
  const title = input.title.trim();
  if (!title) {
    throw new Error("Введите название задачи");
  }

  const description = input.description?.trim() ?? "";
  const data = await request(TASKS_PATH, {
    method: "POST",
    body: JSON.stringify({
      title,
      description: description || null,
    }),
  });

  return normalizeTask(data);
}

export async function toggleTask(task) {
  const data = await request(`${TASKS_PATH}/${task.id}`, {
    method: "PUT",
    body: JSON.stringify({
      title: task.title,
      description: task.description || null,
      is_done: !task.isDone,
    }),
  });

  return normalizeTask(data);
}

export async function updateTask(task, input) {
  const title = input.title.trim();
  if (!title) {
    throw new Error("Название задачи не может быть пустым");
  }

  const description = input.description?.trim() ?? "";
  const data = await request(`${TASKS_PATH}/${task.id}`, {
    method: "PUT",
    body: JSON.stringify({
      title,
      description: description || null,
      is_done: task.isDone,
    }),
  });

  return normalizeTask(data);
}

export async function deleteTask(taskId) {
  await request(`${TASKS_PATH}/${taskId}`, {
    method: "DELETE",
  });
}
