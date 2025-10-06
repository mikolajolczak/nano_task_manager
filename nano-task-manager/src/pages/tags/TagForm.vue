<template>
  <form class="p-3" @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label for="name" class="form-label">Tag Name</label>
      <input id="name" v-model="form.name" type="text" class="form-control" required />
    </div>

    <div class="d-flex justify-content-end gap-2">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
      <button type="submit" class="btn btn-primary">{{ isEdit ? "Update" : "Create" }}</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import type { Tag } from "@/models/Tag";
import { reactive, watch, computed } from "vue";

const props = defineProps<{
  tag?: Tag;
}>();

const emit = defineEmits<{
  (e: "submit", payload: Tag): void;
  (e: "cancel"): void;
}>();

const isEdit = computed(() => !!props.tag);

const form = reactive<Tag>({
  name: "",
  id: "",
});

watch(
  () => props.tag,
  (t) => {
    if (t) Object.assign(form, t);
    else form.name = "";
  },
  { immediate: true }
);

const handleSubmit = () => {
  emit("submit", { ...form });
};
</script>
