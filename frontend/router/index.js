import { createRouter, createWebHistory } from "vue-router";
import StaffView from "../views/StaffView.vue";
import ScheduleView from "../views/ScheduleView.vue";

const routes = [
  { path: "", redirect: "/schedule" },
  { path: "/", redirect: "/schedule" },
  { path: "/staff", component: StaffView },
  { path: "/schedule", component: ScheduleView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
