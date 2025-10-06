<template>
  <form class="p-3" @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label for="name" class="form-label">Project Name</label>
      <input id="name" v-model="form.name" type="text" class="form-control" required />
    </div>

    <div class="mb-3">
      <label for="description" class="form-label">Description</label>
      <textarea
        id="description"
        v-model="form.description"
        class="form-control"
        rows="3"
      ></textarea>
    </div>

    <div class="mb-3">
      <label for="owner" class="form-label">Owner</label>
      <select id="owner" v-model="form.owner_id" class="form-select" required>
        <option v-for="u in users" :key="u.id" :value="u.id">{{ u.name }}</option>
      </select>
    </div>

    <div class="d-flex justify-content-end gap-2">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
      <button type="submit" class="btn btn-primary">{{ isEdit ? "Update" : "Create" }}</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch, computed } from "vue";
import { getUsers } from "@/services/api";
import type { Project } from "@/models/Project";
import type { User } from "@/models/User";

const props = defineProps<{
  project?: Project;
}>();

const emit = defineEmits<{
  (e: "submit", payload: Project): void;
  (e: "cancel"): void;
}>();

const isEdit = computed(() => !!props.project);

const form = reactive<Project>({
  name: "",
  description: "",
  id: "-1",
});

watch(
  () => props.project,
  (p) => {
    if (p) Object.assign(form, p);
    else {
      form.name = "";
      form.description = "";
      form.owner_id = "-1";
    }
  },
  { immediate: true }
);

const users = ref<User[]>([]);

const fetchUsers = async () => {
  users.value = (await getUsers()).data.users;
};

onMounted(fetchUsers);

const handleSubmit = () => {
  emit("submit", { ...form });
};
</script>
