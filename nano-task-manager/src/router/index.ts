import HomePage from "@/pages/HomePage.vue";
import NotFound from "@/pages/NotFound.vue";
import ProjectDetail from "@/pages/projects/ProjectDetail.vue";
import ProjectList from "@/pages/projects/ProjectList.vue";
import TagList from "@/pages/tags/TagList.vue";
import TaskDetail from "@/pages/tasks/TaskDetail.vue";
import TaskList from "@/pages/tasks/TaskList.vue";
import UserDetail from "@/pages/users/UserDetail.vue";
import UserList from "@/pages/users/UserList.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", component: HomePage },
    { path: "/users", component: UserList },
    { path: "/users/:id", component: UserDetail, props: true },
    { path: "/tasks", component: TaskList },
    { path: "/tasks/:id", component: TaskDetail, props: true },
    { path: "/projects", component: ProjectList },
    { path: "/projects/:id", component: ProjectDetail, props: true },
    { path: "/tags", component: TagList },
    { path: "/:pathMatch(.*)*", component: NotFound },
  ],
});

export default router;
