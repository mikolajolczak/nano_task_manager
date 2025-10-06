<template>
  <form class="p-3" @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label for="title" class="form-label">Title</label>
      <input id="title" v-model="form.title" type="text" class="form-control" required />
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
      <label for="status" class="form-label">Status</label>
      <select id="status" v-model="form.status" class="form-select">
        <option value="todo">To Do</option>
        <option value="in_progress">In Progress</option>
        <option value="done">Done</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="assignee" class="form-label">Assignee</label>
      <select id="assignee" v-model="form.assignee_id" class="form-select">
        <option value="">None</option>
        <option v-for="u in users" :key="u.id" :value="u.id">{{ u.name }}</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="project" class="form-label">Project</label>
      <select id="project" v-model="form.project_id" class="form-select" required>
        <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.name }}</option>
      </select>
    </div>

    <div class="mb-3">
      <label class="form-label">Tags</label>
      <div>
        <div v-for="tag in tags" :key="tag.id" class="form-check form-check-inline">
          <input
            :id="'tag-' + tag.id"
            type="checkbox"
            class="form-check-input"
            :checked="form.tags.some((t) => t.id === tag.id)"
            @change="toggleTag(tag)"
          />
          <label class="form-check-label" :for="'tag-' + tag.id">{{ tag.name }}</label>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-end gap-2">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
      <button type="submit" class="btn btn-primary">{{ isEdit ? "Update" : "Create" }}</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted, computed } from "vue";
import { getUsers, getProjects, getTags } from "@/services/api";
import type { User } from "@/models/User";
import type { Task } from "@/models/Task";
import type { Project } from "@/models/Project";
import type { Tag } from "@/models/Tag";

const props = defineProps<{
  task?: Task;
}>();

const emit = defineEmits<{
  (e: "submit", payload:Task): void;
  (e: "cancel"): void;
}>();

const isEdit = computed(() => !!props.task);

const form = reactive<Task>({
  id: "-1",
  title: "",
  description: "",
  status: "todo",
  project_id: "-1",
  assignee_id: null,
  tags: [],
});

watch(
  () => props.task,
  (t) => {
    if (t) {
      form.id = t.id;
      form.title = t.title;
      form.description = t.description ?? "";
      form.status = t.status;
      form.project_id = t.project_id;
      form.assignee_id = t.assignee_id ?? undefined;
      form.tags = [...t.tags];
    } else {
      form.id = "-1";
      form.title = "";
      form.description = "";
      form.status = "todo";
      form.project_id = "-1";
      form.assignee_id = null;
      form.tags = [];
    }
  },
  { immediate: true }
);

const users = ref<User[]>([]);
const projects = ref<Project[]>([]);
const tags = ref<Tag[]>([]);

const fetchOptions = async () => {
  users.value = (await getUsers()).data.users;
  projects.value = (await getProjects()).data.projects;
  tags.value = (await getTags()).data.tags;
};

onMounted(fetchOptions);

const toggleTag = (tag: Tag) => {
  const index = form.tags.findIndex((t) => t.id === tag.id);
  if (index > -1) {
    form.tags.splice(index, 1);
  } else {
    form.tags.push(tag);
  }
};

const handleSubmit = () => {
  const payload = { ...form, tag_ids: form.tags.map((t) => t.id) };
  emit("submit", { ...payload });
};
</script>
