import { createRouter, createWebHistory } from "vue-router";
import DashboardPage from "../pages/DashboardPage.vue";
import NotFoundPage from "../pages/NotFoundPage.vue";

const routes = [
    { path: "/", redirect: "/dashboard" },
    { path: "/dashboard", name: "dashboard", component: DashboardPage },
    { path: "/:pathMatch(.*)*", name: "not-found", component: NotFoundPage },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;