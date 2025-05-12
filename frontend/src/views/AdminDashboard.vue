<template>
  <div class="dashboard p-6 bg-light min-h-screen">
    <div class="flex">
      <!-- Sidebar Component -->
      <Sidebar class="w-1/6 h-screen" />

      <!-- Main content -->
      <div class="w-5/6 px-8">
        <!-- Navbar Component -->
        <Navbar />

        <!-- Subjects Grid Component -->
        <div class="mt-8">
          <Subjects :subjects="subjects" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "@/components/navbar.vue";
import Sidebar from "@/components/sidebar.vue";
import Subjects from "@/views/subjects.vue";

export default {
  name: "AdminDashboard",
  components: {
    Navbar,
    Sidebar,
    Subjects,
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
        const token = localStorage.getItem("access_token"); // ✅ Get JWT from localStorage

        const response = await axios.get(
          "http://localhost:5000/admin/subjects",
          {
            headers: {
              Authorization: `Bearer ${token}`, // ✅ Pass token in request
              "Content-Type": "application/json",
            },
          }
        );

        this.subjects = response.data; // ✅ Assign response to subjects
      } catch (error) {
        console.error("Failed to fetch subjects:", error);
      }
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}
</style>
