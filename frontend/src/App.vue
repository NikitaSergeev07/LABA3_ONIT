<script setup>
import { computed, onMounted, ref } from "vue";

import {
  createTask,
  deleteTask,
  listTasks,
  toggleTask,
  updateTask,
} from "./api";
import TaskForm from "./components/TaskForm.vue";
import TaskList from "./components/TaskList.vue";

const tasks = ref([]);
const isLoading = ref(false);
const isSaving = ref(false);
const error = ref("");
const success = ref("");

const doneCount = computed(() => tasks.value.filter((task) => task.isDone).length);
const activeCount = computed(() => tasks.value.length - doneCount.value);

function resetMessages() {
  error.value = "";
  success.value = "";
}

async function loadTasks() {
  isLoading.value = true;
  resetMessages();
  try {
    tasks.value = await listTasks();
  } catch (err) {
    error.value = err.message;
  } finally {
    isLoading.value = false;
  }
}

async function handleCreate(input) {
  isSaving.value = true;
  resetMessages();
  try {
    const created = await createTask(input);
    tasks.value = [created, ...tasks.value];
    success.value = "Задача создана";
  } catch (err) {
    error.value = err.message;
  } finally {
    isSaving.value = false;
  }
}

async function handleToggle(task) {
  resetMessages();
  try {
    const updated = await toggleTask(task);
    tasks.value = tasks.value.map((item) => (item.id === updated.id ? updated : item));
  } catch (err) {
    error.value = err.message;
  }
}

async function handleUpdate(payload) {
  resetMessages();
  try {
    const target = tasks.value.find((task) => task.id === payload.id);
    if (!target) {
      return;
    }

    const updated = await updateTask(target, {
      title: payload.title,
      description: payload.description,
    });

    tasks.value = tasks.value.map((item) => (item.id === updated.id ? updated : item));
    success.value = "Задача обновлена";
  } catch (err) {
    error.value = err.message;
  }
}

async function handleDelete(taskId) {
  resetMessages();
  try {
    await deleteTask(taskId);
    tasks.value = tasks.value.filter((task) => task.id !== taskId);
    success.value = "Задача удалена";
  } catch (err) {
    error.value = err.message;
  }
}

onMounted(loadTasks);
</script>

<template>
  <main class="page">
    <section class="panel">
      <header class="hero">
        <p class="eyebrow">TaskFlow</p>
        <h1>Трекер задач</h1>
        <p class="meta">
          В работе: <strong>{{ activeCount }}</strong>
          · Закрыто: <strong>{{ doneCount }}</strong>
        </p>
      </header>

      <TaskForm :loading="isSaving" @create="handleCreate" />

      <p v-if="error" class="message error">{{ error }}</p>
      <p v-if="success" class="message success">{{ success }}</p>

      <TaskList
        :tasks="tasks"
        :loading="isLoading"
        @toggle="handleToggle"
        @remove="handleDelete"
        @update="handleUpdate"
      />
    </section>
  </main>
</template>
