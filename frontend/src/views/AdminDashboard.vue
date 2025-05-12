<template>
  <div class="d-flex vh-100 overflow-hidden">
    <!-- Sidebar -->
    <Sidebar class="bg-dark text-white" />

    <!-- Main content area -->
    <div class="flex-grow-1 d-flex flex-column">
      
      <!-- Navbar -->
      <Navbar class="bg-white shadow-sm" />

      <!-- Content area -->
      <div class="flex-grow-1 p-4 bg-light overflow-auto">
        <h2 class="page-title">Subjects</h2>

        <!-- Dynamic Subjects go here -->
        
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import Navbar from "@/components/navbar.vue";
import Sidebar from "@/components/sidebar.vue";

export default {
  name: "AdminDashboard",
  components: {
    Navbar,
    Sidebar,
  },
  data() {
    return {
      subjects: [],
    };
  },
  mounted() {
    this.fetchSubjects();
  },
  methods: {
    async fetchSubjects() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get("http://localhost:5000/admin/subjects", {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        this.subjects = response.data;
      } catch (error) {
        console.error("Failed to fetch subjects:", error);
      }
    },
  },
};
</script>

<style scoped>
.bg-light {
  background-color:rgb(199, 212, 224) !important;
}
.page-title {
  margin-left: 260px; /* same as sidebar width */
  padding-top: 60px;   /* slightly more than navbar height */
  font-size: 2rem;
  color: black;
}

</style>
