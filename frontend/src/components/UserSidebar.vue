<template>
  <div class="bg-dark text-white vh-100 p-3 position-fixed" style="width: 175px;">
    <h5 class="text-center mb-4">User Menu</h5>
    <ul class="nav flex-column">
      <li class="nav-item mb-2">
        <router-link to="/user/dashboard" class="nav-link text-white">🏠 Home</router-link>
      </li>
      <li class="nav-item mb-2">
        <router-link to="/user/subjects" class="nav-link text-white">📚 Subjects</router-link>
      </li>
      <li class="nav-item mb-2">
        <router-link to="/user/reports" class="nav-link text-white">📄 Report</router-link>
      </li>
      <li class="nav-item mb-2">
        <a href="#" class="nav-link text-danger" @click.prevent="logout">🚪 Logout</a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'UserSidebar',
  methods: {
    logout() {
      localStorage.removeItem('access_token')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.nav-link {
  transition: background-color 0.2s;
}
.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
}
</style>
