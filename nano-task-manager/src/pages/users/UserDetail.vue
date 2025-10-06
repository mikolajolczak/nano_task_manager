<template>
  <div class="container py-4">
    <h1 class="mb-4">User Detail</h1>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else-if="!editing">
      <div class="card shadow-sm">
        <div class="card-body">
          <h5 class="card-title">{{ user?.name }}</h5>
          <p class="card-text">
            <strong>Email:</strong>
            {{ user?.email }}
          </p>
          <div class="d-flex gap-2">
            <button class="btn btn-warning" @click="startEdit">Edit</button>
            <button class="btn btn-secondary" @click="goBack">Back</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <UserForm :user="user" @submit="saveUser" @cancel="cancelEdit" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import UserForm from "./UserForm.vue";
import { getUserById, updateUser } from "@/services/api";
import type { User } from "@/models/User";

const route = useRoute();
const router = useRouter();

const user = ref<User | undefined>(undefined);
const loading = ref(false);
const error = ref<string | null>(null);
const editing = ref(false);

const fetchUser = async () => {
  loading.value = true;
  try {
    const id = route.params.id as string;
    const res = await getUserById(id);
    user.value = res.data;
  } catch (err) {
    console.error(err);
    error.value = "Failed to fetch user.";
  } finally {
    loading.value = false;
  }
};

const startEdit = () => {
  editing.value = true;
};

const cancelEdit = () => {
  editing.value = false;
};

const saveUser = async (formData: { name: string; email: string }) => {
  if (!user.value) return;
  try {
    await updateUser(user.value.id, { id: user.value.id, ...formData });
    user.value = { ...user.value, ...formData };
    editing.value = false;
  } catch (err) {
    console.error(err);
    alert("Failed to update user.");
  }
};

const goBack = async () => {
  await router.push("/users");
};

onMounted(fetchUser);
</script>
<style scoped>
.container {
  max-width: 80vw;
}
</style>
