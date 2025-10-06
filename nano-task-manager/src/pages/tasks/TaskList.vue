<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Tasks</h1>
      <button class="btn btn-primary" @click="startCreate">+ Add Task</button>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <table class="table table-striped table-hover">
        <thead class="table-primary">
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Status</th>
            <th>Project</th>
            <th>Assignee</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in tasks" :key="t.id">
            <td>{{ t.id }}</td>
            <td>{{ t.title }}</td>
            <td>{{ t.status }}</td>
            <td>{{ t.project_id }}</td>
            <td>{{ t.assignee_id || "None" }}</td>
            <td>
              <button class="btn btn-sm btn-info me-2" @click="goToDetail(t.id)">View</button>
              <button class="btn btn-sm btn-warning me-2" @click="startEdit(t)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="handleDelete(t.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="tasks.length === 0" class="alert alert-warning">No tasks found.</div>
    </div>

    <div id="taskModal" ref="modalRef" class="modal fade" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingTask ? "Edit Task" : "Add Task" }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <TaskForm :task="editingTask" @submit="handleFormSubmit" @cancel="closeModal" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import TaskForm from "./TaskForm.vue";
import { getTasks, createTask, updateTask, deleteTask as apiDeleteTask } from "@/services/api";
import type { Task } from "@/models/Task";
import { Modal } from "bootstrap";

const tasks = ref<Task[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const editingTask = ref<Task | undefined>(undefined);
const modalRef = ref<HTMLDivElement | null>(null);

let bootstrapModal: Modal | null = null;

const router = useRouter();

const fetchTasks = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await getTasks();
    tasks.value = res.data.tasks;
  } catch (err) {
    console.error(err);
    error.value = "Failed to fetch tasks.";
  } finally {
    loading.value = false;
  }
};

const goToDetail = (id: string) => router.push(`/tasks/${id}`);

const startCreate = () => {
  editingTask.value = undefined;
  showModal();
};

const startEdit = (task: Task) => {
  editingTask.value = { ...task };
  showModal();
};

const handleFormSubmit = async (data: Task) => {
  try {
    if (editingTask.value) {
      await updateTask(editingTask.value.id, data);
    } else {
      await createTask(data);
    }
    closeModal();
    await fetchTasks();
  } catch (err) {
    console.error(err);
    alert("Failed to save task.");
  }
};

const handleDelete = async (id: string) => {
  if (!confirm("Are you sure you want to delete this task?")) return;
  try {
    await apiDeleteTask(id);
    await fetchTasks();
  } catch (err) {
    console.error(err);
    alert("Failed to delete task.");
  }
};

const showModal = () => {
  if (modalRef.value) {
    bootstrapModal ??= new Modal(modalRef.value);
    bootstrapModal.show();
  }
};

const closeModal = () => {
  if (bootstrapModal) {
    bootstrapModal.hide();
  }
};

onMounted(fetchTasks);
</script>

<style scoped>
.container {
  max-width: 960px;
}
</style>
