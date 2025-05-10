<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/login.vue";
import Register from "./components/register.vue";

const routes = [
  { path: "/login", component: Login },
  { path: "/register", component: Register },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default {
  name: "App",
  router,
};
</script>
