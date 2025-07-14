<template>
  <div
    class="custom-sidebar text-white vh-100 p-3 position-fixed"
    style="width: 175px"
  >
    <h5 class="text-center mb-4">User Menu</h5>
    <ul class="nav flex-column">
      <li class="nav-item mb-2">
        <router-link to="/user/dashboard" class="nav-link text-white"
          >🏠 Home</router-link
        >
      </li>
      <li class="nav-item mb-2">
        <router-link to="/user/subjects" class="nav-link text-white"
          >📚 Subjects</router-link
        >
      </li>
      <li class="nav-item mb-2">
        <router-link to="/user/score/history" class="nav-link text-white"
          >📘 Quiz History</router-link
        >
      </li>

      <li class="nav-item mb-2">
        <router-link to="/user/summary" class="nav-link text-white"
          >📄 Quiz Report</router-link
        >
      </li>
      <li class="nav-item mb-2">
        <a href="#" class="nav-link text-danger" @click.prevent="logout"
          >🚪 Logout</a
        >
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "UserSidebar",
  methods: {
    logout() {
      localStorage.removeItem("access_token");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.nav-link {
  padding: 12px 16px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav-link:hover {
  background-color: #064c74ff;
  color: #ffffff;
  border-radius: 6px;
}

.router-link-exact-active {
  background-color: #064c74ff ;
  font-weight: 600;
  border-radius: 6px;
}

.custom-sidebar {
 background-color: #032d45 !important;
}
</style>
