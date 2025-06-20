<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-4">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <!-- Welcome message -->
      <span class="navbar-brand mb-0 h5">Welcome QuizMaster✨</span>

      <!-- Search bar -->
      <form class="d-flex w-50" @submit.prevent="performSearch">
        <input
          v-model="searchQuery"
          class="form-control me-2"
          type="search"
          placeholder="Search quizzes or subjects..."
          aria-label="Search"
        />
        <button class="btn btn-outline-primary" type="submit">Search</button>
      </form>
    </div>
  </nav>
</template>

<script>
export default {
  name: "UserNavbar",
  data() {
    return {
      searchQuery: "", // 🔍 Search input binding
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
