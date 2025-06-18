import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/login.vue";
import Register from "../components/register.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import SubjectDetail from "@/views/SubjectDetail.vue";
import UserSubjects from "@/views/UserSubjects.vue";
import UserSubjectDetail from "@/views/UserSubjectDetail.vue";
import UserDashboard from "@/views/UserDashboard.vue";
import QuizList from "@/views/QuizList.vue";
import Users from "../components/Users.vue";
const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  {
    path: "/users",
    component: Users,
  },
  {
    path: "/dashboard",
    component: AdminDashboard,
  },
  {
    path: "/admin/subject/:subjectId",
    name: "SubjectDetail",
    component: SubjectDetail,
    props: true, // This allows us to pass route params as props
  },
  {
    path: "/admin/chapter/:chapterId/quizzes",
    name: "QuizList",
    component: QuizList,
    props: (route) => ({
      chapterId: Number(route.params.chapterId),
      chapterName: route.params.chapterName,
    }),
  },
  {
    path: "/admin/quizzes/:quizId/questions",
    name: "QuizQuestions",
    component: () => import("@/views/QuestionList.vue"),
    props: true,
  },
  {
    path: "/user/dashboard",
    name: "UserDashboard",
    component: UserDashboard,
  },
  {
    path: "/user/subjects",
    name: "UserSubjects",
    component: UserSubjects,
  },
  {
    path: "/user/subject/:subjectId",
    name: "UserSubjectDetail",
    component: UserSubjectDetail,
    props: true,
  },
  {
    path: "/user/quiz/:quizId/attempt",
    name: "QuizAttempt",
    component: () => import("@/views/QuizAttempt.vue"),
    props: (route) => ({
      quizId: route.params.quizId,
      subjectId: route.query.subjectId || null,
    }),
  },

  {
    path: "/user/scorecard/:score_id",
    name: "ScoreCard",
    component: () => import("@/views/ScoreCard.vue"),
    props: true,
  },
  {
    path: "/user/score/history",
    name: "QuizHistory",
    component: () => import("@/views/QuizHistory.vue"),
  },
  {
    path: "/user/summary",
    name: "QuizSummary",
    component: () => import("@/views/QuizSummary.vue"),
  },
  {
    path: "/admin/search",
    name: "AdminSearch",
    component: () => import("@/views/AdminSearch.vue"),
    
  },
  {
    path: "/user/search",
    name: "UserSearch",
    component: () => import("@/views/UserSearch.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
