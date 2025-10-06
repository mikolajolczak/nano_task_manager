<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Users</h1>
      <button class="btn btn-primary" @click="startCreate">+ Add User</button>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <table class="table table-hover table-striped">
        <thead class="table-primary">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.id }}</td>
            <td>{{ u.name }}</td>
            <td>{{ u.email }}</td>
            <td class="d-flex justify-content-center">
              <button class="btn btn-sm btn-info me-2" @click="goToDetail(u.id)">View</button>
              <button class="btn btn-sm btn-warning me-2" @click="startEdit(u)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteUser(u.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="users.length === 0" class="alert alert-warning">No users found.</div>
    </div>

    <div
      id="userModal"
      ref="modalRef"
      class="modal fade"
      tabindex="-1"
      aria-labelledby="userModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 id="userModalLabel" class="modal-title">
              {{ editingUser ? "Edit User" : "Add User" }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <UserForm :user="editingUser" @submit="handleFormSubmit" @cancel="closeModal" />
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
          <div class="modal-body">Are you sure you want to delete this user?</div>
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
import { useRouter } from "vue-router";
import { getUsers, createUser, updateUser, deleteUser as apiDeleteUser } from "@/services/api";
import UserForm from "./UserForm.vue";
import { Modal } from "bootstrap";
import type { User } from "@/models/User";

const users = ref<User[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const router = useRouter();

const modalRef = ref<HTMLDivElement | null>(null);
let bootstrapModal: Modal | null = null;
const deleteModalRef = ref<HTMLDivElement | null>(null);
let bootstrapDeleteModal: Modal | null = null;
let userIdToDelete: string | null = null;

const editingUser = ref<User | undefined>(undefined);

const fetchUsers = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await getUsers();
    users.value = res.data.users;
  } catch (err) {
    console.error(err);
    error.value = "Failed to fetch users.";
  } finally {
    loading.value = false;
  }
};

const goToDetail = async (id: string) => {
  await router.push(`/users/${id}`);
};

const startCreate = () => {
  editingUser.value = undefined;
  showModal();
};

const startEdit = (user: User) => {
  editingUser.value = { ...user };
  showModal();
};

const handleFormSubmit = async (formData: { name: string; email: string }) => {
  try {
    if (editingUser.value) {
      await updateUser(editingUser.value.id, { id: editingUser.value.id, ...formData });
    } else {
      await createUser({ id: "-1", ...formData });
    }
    closeModal();
    await fetchUsers();
  } catch (err) {
    console.error(err);
    alert("Failed to save user.");
  }
};

const deleteUser = (id: string) => {
  userIdToDelete = id;
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
  if (!userIdToDelete) return;
  try {
    await apiDeleteUser(userIdToDelete);
    await fetchUsers();
  } catch (err) {
    console.error(err);
    alert("Failed to delete user.");
  } finally {
    closeDeleteModal();
    userIdToDelete = null;
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

onMounted(fetchUsers);
</script>

<style scoped>
.container {
  max-width: 80vw;
}
</style>
