<template>
  <nav
    class="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-4"
    style="height: 60px; z-index: 1000"
  >
    <div
      class="container-fluid d-flex justify-content-between align-items-center"
    >
      <!-- Logo -->
      <span class="navbar-brand fw-bold">Quiz Master</span>

      <!-- Search Bar -->
      <input
        type="text"
        class="form-control"
        placeholder="Search..."
        style="max-width: 600px"
      />
    </div>
  </nav>
</template>

<script>
export default {
  name: "Navbar",
};
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 260px; /* same as sidebar width */
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
