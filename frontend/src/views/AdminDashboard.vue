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

        <!-- Dynamic Subjects -->
        <div class="subject-cards-container">
          <div
            v-for="subject in subjects"
            :key="subject.subject_id"
            class="subject-card"
          >
            <router-link :to="'/admin/subject/' + subject.subject_id">
              <h4>{{ subject.name }}</h4>
              <p>{{ subject.description }}</p>
            </router-link>
          </div>
        </div>

        <!-- Dynamic Subjects go here -->

        <!-- Floating Create Subject Button -->
        <button class="create-subject-btn" @click="showForm = !showForm">
          + Create Subject
        </button>

        <!-- Create Subject Modal Dialog -->
        <div
          v-if="showForm"
          class="modal-overlay"
          @click.self="showForm = false"
        >
          <div class="modal-content">
            <h3>Create Subject</h3>
            <input v-model="newSubject.name" placeholder="Subject Name" />
            <input v-model="newSubject.description" placeholder="Description" />
            <div class="modal-actions">
              <button @click="createSubject">Submit</button>
              <button @click="showForm = false">Cancel</button>
            </div>
          </div>
        </div>
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
      showForm: false,
      newSubject: {
        name: "",
        description: "",
      },
      subjects: [],
    };
  },
  methods: {
    async fetchSubjects() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          "http://localhost:5000/admin/subjects",
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
        this.subjects = response.data;
      } catch (error) {
        console.error("Failed to fetch subjects:", error);
      }
    },
    async createSubject() {
      const { name, description } = this.newSubject;

      if (!name || !description) return;

      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.post(
          "http://localhost:5000/admin/subjects",
          {
            name,
            description,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        // Push the newly created subject from backend response
        this.subjects.push(response.data);

        // Reset form and close modal
        this.newSubject = { name: "", description: "" };
        this.showForm = false;
      } catch (error) {
        console.error("Error creating subject:", error);
      }
    },
  },
  mounted() {
    this.fetchSubjects();
  },
};
</script>

<style scoped>
.bg-light {
  background-color: rgb(242, 245, 247) !important;
}
.page-title {
  margin-left: 260px; /* same as sidebar width */
  padding-top: 60px; /* slightly more than navbar height */
  font-size: 2rem;
  color: black;
}
.create-subject-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: rgb(60, 60, 61);
  color: white;
  padding: 12px 18px;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.75);
  cursor: pointer;
}

.subject-form {
  position: fixed;
  bottom: 80px;
  right: 20px;
  background-color: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(22, 21, 21, 0.95);
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1000;
}

.subject-form input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background-color: white;
  padding: 16px 20px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
  width: 350px; /* Set fixed small width */
  min-height: 200px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.modal-content h3 {
  margin: 0 0 12px 0;
  font-size: 1.2rem;
  color: #333;
  text-align: center;
}

.modal-content input {
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 0.95rem;
  border: 1px solid #ccc;
  width: 100%; /* Ensures inputs stay within the modal */
  box-sizing: border-box;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}

.modal-actions button {
  padding: 6px 12px;
  font-size: 0.9rem;
  border-radius: 6px;
  border: none;
  background-color: #333;
  color: white;
  cursor: pointer;
}

.subject-cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-left: 260px; /* same as sidebar width */
  margin-top: 20px;
}

.subject-card {
  background-color: white;
  padding: 16px 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  width: 250px;
  min-height: 120px;
}
</style>
