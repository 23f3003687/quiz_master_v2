<template>
  <div class="bg-dark text-white p-3">
    <h4 class="fw-bold mb-4 mt-1">Admin Panel</h4>
    <ul class="nav flex-column gap-2">
      <li class="nav-item">
        <router-link to="/dashboard" class="nav-link text-white">
          <i class="bi bi-house-door"></i> Home
        </router-link>
      </li>
      <li class="nav-item">
        <router-link to="/admin/users" class="nav-link text-white">
          <i class="bi bi-people"></i> Users
        </router-link>
      </li>
      <li class="nav-item">
        <router-link to="/admin/summary" class="nav-link text-white">
          <i class="bi bi-graph-up"></i> Summary
        </router-link>
      </li>
      <li class="nav-item">
        <a class="nav-link text-danger" href="#" @click.prevent="logout">
          <i class="bi bi-box-arrow-right"></i> Logout
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Sidebar",
  methods: {
    logout() {
      localStorage.removeItem("access_token"); // Clear JWT token
      this.$router.push("/login"); // Navigate to login page
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 175px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 998;
}
</style>
