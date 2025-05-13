import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/login.vue";
import Register from "../components/register.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import SubjectDetail from '@/views/SubjectDetail.vue';
const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  {
    path: "/dashboard",
    component: AdminDashboard,
  },
  {
    path: '/admin/subject/:subjectId',
    name: 'SubjectDetail',
    component: SubjectDetail,
    props: true, // This allows us to pass route params as props
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
