<script setup>
import { reactive } from "vue";

const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["create"]);

const form = reactive({
  title: "",
  description: "",
});

function submitForm() {
  emit("create", {
    title: form.title,
    description: form.description,
  });

  form.title = "";
  form.description = "";
}
</script>

<template>
  <form class="task-form" @submit.prevent="submitForm">
    <label>
      <span>Название</span>
      <input
        v-model="form.title"
        :disabled="props.loading"
        maxlength="150"
        placeholder="Например: Подготовить отчет"
        required
      />
    </label>

    <label>
      <span>Описание</span>
      <textarea
        v-model="form.description"
        :disabled="props.loading"
        maxlength="1000"
        placeholder="Кратко опишите задачу"
      />
    </label>

    <button :disabled="props.loading" type="submit">
      {{ props.loading ? "Сохраняю..." : "Добавить задачу" }}
    </button>
  </form>
</template>
