<template>
  <div class="container py-4">
    <h1>Task Detail</h1>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else-if="!editing">
      <div class="card shadow-sm">
        <div class="card-body">
          <h5 class="card-title">{{ task?.title }}</h5>
          <p>{{ task?.description }}</p>
          <p>
            <strong>Status:</strong>
            {{ task?.status }}
          </p>
          <p>
            <strong>Project:</strong>
            {{ task?.project_id }}
          </p>
          <p>
            <strong>Assignee:</strong>
            {{ task?.assignee_id || "None" }}
          </p>
          <p>
            <strong>Tags:</strong>
            <span v-for="t in task?.tags" :key="t.id">{{ t.name }}</span>
          </p>
          <div class="d-flex gap-2">
            <button class="btn btn-warning" @click="editing = true">Edit</button>
            <button class="btn btn-secondary" @click="goBack">Back</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <TaskForm :task="task" @submit="saveTask" @cancel="cancelEdit" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import TaskForm from "./TaskForm.vue";
import { getTaskById, updateTask } from "@/services/api";
import type { Task } from "@/models/Task";

const route = useRoute();
const router = useRouter();

const task = ref<Task | undefined>(undefined);
const loading = ref(false);
const error = ref<string | null>(null);
const editing = ref(false);

const fetchTask = async () => {
  loading.value = true;
  try {
    const id = route.params.id as string;
    task.value = (await getTaskById(id)).data;
  } catch (err) {
    console.error(err);
    error.value = "Failed to fetch task.";
  } finally {
    loading.value = false;
  }
};

const goBack = () => router.push("/tasks");
const cancelEdit = () => (editing.value = false);
const saveTask = async (data: Task) => {
  if (!task.value) return;
  await updateTask(task.value.id, data);
  Object.assign(task.value, data);
  editing.value = false;
};

onMounted(fetchTask);
</script>
