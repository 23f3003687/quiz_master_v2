<template>
  <div class="d-flex vh-100 overflow-hidden">
    <!-- Sidebar on the left -->
    <Sidebar class="bg-dark text-white" />

    <!-- Main content on the right -->
    <div class="flex-grow-1 d-flex flex-column">
      <!-- Navbar at the top -->
      <Navbar class="bg-white shadow-sm" />

      <!-- Page content -->
      <div class="container mt-5 pt-3">
        <h2 class="mt-3 mb-3">Registered Users</h2>

        <div
          class="table-responsive text-white"
        >
          <table class="table table-hover align-middle shadow-sm rounded">
            <thead class="custom-thead">
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Full Name</th>
                <th scope="col">Email</th>
                <th scope="col">Qualification</th>
                <th scope="col">DOB</th>
                <th scope="col">Role</th>
                <th scope="col">Last Login</th>
                <th scope="col">Registered On</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(user, index) in users"
                :key="user.user_id"
                :class="{ 'table-info': user.is_admin }"
              >
                <td>{{ index + 1 }}</td>
                <td class="fw-semibold">{{ user.full_name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.qualification || "—" }}</td>
                <td>{{ formatDate(user.dob) }}</td>
                <td>
                  <span
                    class="badge"
                    :class="user.is_admin ? 'bg-primary' : 'bg-secondary'"
                  >
                    {{ user.is_admin ? "Admin" : "User" }}
                  </span>
                </td>
                <td>{{ formatDateTime(user.last_login) || "—" }}</td>
                <td>{{ formatDateTime(user.registered_on) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="errorMessage" class="alert alert-danger mt-3">
          {{ errorMessage }}
        </div>
      </div>
    </div>
    <!-- End of main content -->
  </div>
  <!-- End of main container -->
</template>

<script>
import axios from "axios";
import Navbar from "@/components/navbar.vue";
import Sidebar from "@/components/sidebar.vue";

export default {
  name: "Users",
  components: {
    Sidebar,
    Navbar,
  },
  data() {
    return {
      users: [],
      errorMessage: "",
    };
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return "—";
      return new Date(dateStr).toLocaleDateString();
    },
    formatDateTime(dateTimeStr) {
      if (!dateTimeStr) return null;
      return new Date(dateTimeStr).toLocaleString();
    },
  },
  async mounted() {
    const token = localStorage.getItem("access_token");
    try {
      const response = await axios.get("http://localhost:5000/admin/users", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      this.users = response.data;
    } catch (error) {
      console.error("Failed to fetch users", error);
      this.errorMessage = "Failed to fetch users. Please try again later.";
    }
  },
};
</script>

<style scoped>
.table {
  border-radius: 8px;
  overflow: hidden;
  font-size: 0.95rem;
}

.table th,
.table td {
  vertical-align: middle;
  text-align: center;
}

.badge {
  font-size: 0.85rem;
  padding: 6px 10px;
  border-radius: 12px;
}

.container {
  background-color: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(192, 177, 177, 0.05);
}

/* ✅ Add this */
.custom-thead,
.custom-thead th {
  background-color: #032d45 !important;
  color: white !important;
}
</style>
