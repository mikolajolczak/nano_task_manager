import HomePage from "@/pages/HomePage.vue";
import UserDetail from "@/pages/users/UserDetail.vue";
import UserList from "@/pages/users/UserList.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", component: HomePage },
    { path: "/users", component: UserList },
    {path: "/users/:id", component: UserDetail, props: true},
    { path: "/:pathMatch(.*)*", redirect: "/" },
  ],
});

export default router;
