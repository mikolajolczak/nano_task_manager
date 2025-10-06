<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Tags</h1>
      <button class="btn btn-primary" @click="startCreate">+ Add Tag</button>
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
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in tags" :key="t.id">
            <td>{{ t.id }}</td>
            <td>{{ t.name }}</td>
            <td>
              <button class="btn btn-sm btn-warning me-2" @click="startEdit(t)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteTag(t.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="tags.length === 0" class="alert alert-warning">No tags found.</div>
    </div>

    <div id="tagModal" ref="modalRef" class="modal fade" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingTag ? "Edit Tag" : "Add Tag" }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <TagForm :tag="editingTag" @submit="handleFormSubmit" @cancel="closeModal" />
          </div>
        </div>
      </div>
    </div>
        <div
      id="confirmDeleteModal"
      ref="deleteModalRef"
      class="modal fade"
      tabindex="-1"
      aria-labelledby="confirmDeleteLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 id="confirmDeleteLabel" class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" @click="closeDeleteModal"></button>
          </div>
          <div class="modal-body">Are you sure you want to delete this tag?</div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeDeleteModal">Cancel</button>
            <button class="btn btn-danger" @click="confirmDelete">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import TagForm from "./TagForm.vue";
import { getTags, createTag, updateTag, deleteTag as apiDeleteTag } from "@/services/api";
import type { Tag } from "@/models/Tag";
import { Modal } from "bootstrap";

const tags = ref<Tag[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const editingTag = ref<Tag | undefined>(undefined);
const modalRef = ref<HTMLDivElement | null>(null);

const deleteModalRef = ref<HTMLDivElement | null>(null);
let bootstrapDeleteModal: Modal | null = null;
let tagIdToDelete: string | null = null;


let bootstrapModal: Modal | null = null;

const fetchTags = async () => {
  loading.value = true;
  error.value = null;
  try {
    tags.value = (await getTags()).data.tags;
  } catch (err) {
    console.error(err);
    error.value = "Failed to fetch tags.";
  } finally {
    loading.value = false;
  }
};

const startCreate = () => {
  editingTag.value = undefined;
  showModal();
};

const startEdit = (t: Tag) => {
  editingTag.value = { ...t };
  showModal();
};

const handleFormSubmit = async (data: Tag) => {
  try {
    if (editingTag.value) {
      await updateTag(editingTag.value.id, data);
    } else {
      await createTag(data);
    }
    closeModal();
    await fetchTags();
  } catch (err) {
    console.error(err);
    alert("Failed to save tag.");
  }
};
const deleteTag = (id: string) => {
  tagIdToDelete = id;
  showDeleteModal();
};

const showDeleteModal = () => {
  if (deleteModalRef.value) {
    bootstrapDeleteModal ??= new Modal(deleteModalRef.value);
    bootstrapDeleteModal.show();
  }
};

const closeDeleteModal = () => {
  if (bootstrapDeleteModal) {
    bootstrapDeleteModal.hide();
  }
};

const confirmDelete = async () => {
  if (!tagIdToDelete) return;
  try {
    await apiDeleteTag(tagIdToDelete);
    await fetchTags();
  } catch (err) {
    console.error(err);
    alert("Failed to delete user.");
  } finally {
    closeDeleteModal();
    tagIdToDelete = null;
  }
};

const showModal = () => {
  if (modalRef.value) {
    bootstrapModal ??= new Modal(modalRef.value);
    bootstrapModal.show();
  }
};

const closeModal = () => bootstrapModal?.hide();

onMounted(fetchTags);
</script>

<style scoped>
.container {
  max-width: 80vw;
}
</style>
