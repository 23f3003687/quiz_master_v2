<template>
  <nav
    class="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-4"
    style="height: 60px; z-index: 999"
  >
    <div
      class="container-fluid d-flex justify-content-between align-items-center"
    >
      <!-- Logo -->
      <span class="navbar-brand fw-bold">Quiz Master</span>

      <!-- Search Bar -->
      <div
        class="d-flex align-items-center gap-2"
        style="max-width: 600px; width: 100%"
      >
        <input
          type="text"
          class="form-control"
          v-model="query"
          @keyup.enter="performSearch"
          placeholder="Search anything like 'users', 'algebra', 'questions'..."
        />
        <button class="btn btn-outline-primary" @click="performSearch">
          Search
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "AdminNavbar",
  data() {
    return {
      query: "",
    };
  },
  methods: {
    performSearch() {
      if (this.query.trim()) {
        this.$router.push({
          name: "AdminSearch",
          query: { query: this.query.trim() },
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
