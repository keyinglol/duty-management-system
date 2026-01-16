import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../../views/Dashboard.vue';
import StaffView from '../../views/StaffView.vue';
import ScheduleView from '../../views/ScheduleView.vue';

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/staff',
    name: 'StaffManagement',
    component: StaffView
  },
  {
    path: '/schedule',
    name: 'ScheduleManagement',
    component: ScheduleView
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;