<template>
  <nav
    class="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-4"
    tyle="height: 100px; z-index: 999"
  >
    <div
      class="container-fluid d-flex justify-content-between align-items-center"
    >
      <!-- Logo -->
      <img
        :src="logo"
        alt="Quiz Master"
        style="max-height: 100px"
      />

      <!-- Search bar -->
      <div
        class="d-flex align-items-center gap-2"
        style="max-width: 600px; width: 100%"
      >
        <input
          v-model="searchQuery"
          class="form-control me-2"
          type="search"
          placeholder="Search quizzes or subjects..."
          aria-label="Search"
        />
        <button class="btn btn-outline-primary" @click="performSearch">
          Search
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import logo from "@/assets/logo.png";
export default {
  name: "UserNavbar",
  data() {
    return {
      searchQuery: "", // 🔍 Search input binding
      logo,
    };
  },
  methods: {
    logout() {
      localStorage.removeItem("access_token");
      this.$router.push("/login");
    },
    performSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push({
          name: "UserSearch",
          query: { query: this.searchQuery.trim() },
        });
      }
    },
  },
};
</script>
<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 175px; /* same as sidebar width */
  right: 0;
  height: 60px;
  background-color: white;
  border-bottom: 1px solid #ddd;
  z-index: 1000;
  padding: 0 1rem;
  display: flex;
  align-items: center;
}
</style>