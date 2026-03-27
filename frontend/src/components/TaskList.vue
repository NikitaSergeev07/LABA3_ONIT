<script setup>
import { reactive } from "vue";

const props = defineProps({
  tasks: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["toggle", "remove", "update"]);

const editState = reactive({
  id: null,
  title: "",
  description: "",
});

function startEdit(task) {
  editState.id = task.id;
  editState.title = task.title;
  editState.description = task.description;
}

function cancelEdit() {
  editState.id = null;
  editState.title = "";
  editState.description = "";
}

function saveEdit(id) {
  emit("update", {
    id,
    title: editState.title,
    description: editState.description,
  });
  cancelEdit();
}
</script>

<template>
  <section class="task-list">
    <p v-if="props.loading" class="placeholder">Загрузка задач...</p>
    <p v-else-if="props.tasks.length === 0" class="placeholder">
      Пока пусто. Добавьте первую задачу.
    </p>

    <ul v-else>
      <li v-for="task in props.tasks" :key="task.id" :class="{ done: task.isDone }">
        <div v-if="editState.id === task.id" class="edit-mode">
          <input v-model="editState.title" maxlength="150" required />
          <textarea v-model="editState.description" maxlength="1000" />
          <div class="actions">
            <button type="button" @click="saveEdit(task.id)">Сохранить</button>
            <button type="button" class="ghost" @click="cancelEdit">Отмена</button>
          </div>
        </div>

        <div v-else class="view-mode">
          <div class="task-content">
            <p class="title">{{ task.title }}</p>
            <p v-if="task.description" class="description">{{ task.description }}</p>
          </div>

          <div class="actions">
            <button type="button" class="ghost" @click="emit('toggle', task)">
              {{ task.isDone ? "Вернуть" : "Выполнить" }}
            </button>
            <button type="button" class="ghost" @click="startEdit(task)">Изменить</button>
            <button type="button" class="danger" @click="emit('remove', task.id)">
              Удалить
            </button>
          </div>
        </div>
      </li>
    </ul>
  </section>
</template>
