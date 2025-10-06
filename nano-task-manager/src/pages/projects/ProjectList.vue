<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Projects</h1>
      <button class="btn btn-primary" @click="startCreate">+ Add Project</button>
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
            <th>Name</th>
            <th>Owner</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in projects" :key="p.id">
            <td>{{ p.id }}</td>
            <td>{{ p.name }}</td>
            <td>{{ p.owner_id }}</td>
            <td>
              <button class="btn btn-sm btn-info me-2" @click="goToDetail(p.id)">View</button>
              <button class="btn btn-sm btn-warning me-2" @click="startEdit(p)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="handleDelete(p.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="projects.length === 0" class="alert alert-warning">No projects found.</div>
    </div>

    <div id="projectModal" ref="modalRef" class="modal fade" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingProject ? "Edit Project" : "Add Project" }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <ProjectForm
              :project="editingProject"
              @submit="handleFormSubmit"
              @cancel="closeModal"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import ProjectForm from "./ProjectForm.vue";
import {
  getProjects,
  createProject,
  updateProject,
  deleteProject as apiDeleteProject,
} from "@/services/api";
import type { Project } from "@/models/Project";
import { Modal } from "bootstrap";

const projects = ref<Project[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const editingProject = ref<Project | undefined>(undefined);
const modalRef = ref<HTMLDivElement | null>(null);
let bootstrapModal: Modal | null = null;

const router = useRouter();

const fetchProjects = async () => {
  loading.value = true;
  error.value = null;
  try {
    projects.value = (await getProjects()).data.projects;
  } catch (err) {
    console.error(err);
    error.value = "Failed to fetch projects.";
  } finally {
    loading.value = false;
  }
};

const goToDetail = (id: string) => router.push(`/projects/${id}`);

const startCreate = () => {
  editingProject.value = undefined;
  showModal();
};

const startEdit = (p: Project) => {
  editingProject.value = { ...p };
  showModal();
};

const handleFormSubmit = async (data: Project) => {
  try {
    if (editingProject.value) {
      await updateProject(editingProject.value.id, data);
    } else {
      await createProject(data);
    }
    closeModal();
    await fetchProjects();
  } catch (err) {
    console.error(err);
    alert("Failed to save project.");
  }
};

const handleDelete = async (id: string) => {
  if (!confirm("Are you sure you want to delete this project?")) return;
  try {
    await apiDeleteProject(id);
    await fetchProjects();
  } catch (err) {
    console.error(err);
    alert("Failed to delete project.");
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

onMounted(fetchProjects);
</script>

<style scoped>
.container {
  max-width: 960px;
}
</style>
