<template>
<div class="bg-dark text-white p-3 vh-100" style="width: 256px; min-width: 256px;">
    <h4 class="fw-bold mb-4 mt-1">Admin Panel</h4>
    <ul class="nav flex-column gap-2">
      <li class="nav-item">
        <router-link to="/admin/subjects" class="nav-link text-white">
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

<style scoped>
.sidebar {
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
}
</style>
