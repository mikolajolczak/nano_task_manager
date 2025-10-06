<template>
  <form class="p-3" @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label for="name" class="form-label">Name</label>
      <input id="name" v-model="form.name" type="text" class="form-control" required />
    </div>

    <div class="mb-3">
      <label for="email" class="form-label">Email</label>
      <input id="email" v-model="form.email" type="email" class="form-control" required />
    </div>

    <div class="d-flex justify-content-end gap-2">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
      <button type="submit" class="btn btn-primary">
        {{ isEdit ? "Update" : "Create" }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import type { User } from "@/models/User";
import { reactive, watch, defineProps, defineEmits, computed } from "vue";

const props = defineProps<{
  user?: User;
}>();

const emit = defineEmits<{
  (e: "submit", payload: User): void;
  (e: "cancel"): void;
}>();

const form = reactive<User>({
  id: props.user?.id ?? "-1",
  name: "",
  email: "",
});

const isEdit = computed(() => !!props.user);

watch(
  () => props.user,
  (newUser) => {
    if (newUser) {
      form.name = newUser.name;
      form.email = newUser.email;
    } else {
      form.name = "";
      form.email = "";
    }
  },
  { immediate: true }
);

const handleSubmit = () => {
  emit("submit", { ...form });
};
</script>
