<template>
  <div class="container py-4">
    <h1>Project Detail</h1>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else-if="!editing">
      <div class="card shadow-sm">
        <div class="card-body">
          <h5 class="card-title">{{ project?.name }}</h5>
          <p>{{ project?.description }}</p>
          <p>
            <strong>Owner:</strong>
            {{ project?.owner?.name }}
          </p>
          <div class="d-flex gap-2">
            <button class="btn btn-warning" @click="editing = true">Edit</button>
            <button class="btn btn-secondary" @click="goBack">Back</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <ProjectForm :project="project" @submit="saveProject" @cancel="cancelEdit" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import ProjectForm from "./ProjectForm.vue";
import { getProjectById, updateProject } from "@/services/api";
import type { Project } from "@/models/Project";

const route = useRoute();
const router = useRouter();

const project = ref<Project | undefined>(undefined);
const loading = ref(false);
const error = ref<string | null>(null);
const editing = ref(false);

const fetchProject = async () => {
  loading.value = true;
  try {
    const id = route.params.id as string;
    project.value = (await getProjectById(id)).data;
  } catch (err) {
    console.error(err);
    error.value = "Failed to fetch project.";
  } finally {
    loading.value = false;
  }
};

const goBack = () => router.push("/projects");
const cancelEdit = () => (editing.value = false);

const saveProject = async (data: Project) => {
  if (!project.value) return;
  await updateProject(project.value.id, data);
  Object.assign(project.value, data);
  editing.value = false;
};

onMounted(fetchProject);
</script>
