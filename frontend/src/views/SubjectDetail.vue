<template>
  <div class="d-flex vh-100 overflow-hidden">
    <!-- Sidebar on the left -->
    <Sidebar class="bg-dark text-white" />

    <!-- Main content on the right -->
    <div class="flex-grow-1 d-flex flex-column">
      <!-- Navbar at the top -->
      <Navbar class="bg-white shadow-sm" />

      <!-- Page content below navbar -->
      <div class="container mt-4 pt-5 flex-grow-1 overflow-auto">
        <!-- Subject Header -->
        <div class="mb-4">
          <h2 class="fw-bold">{{ subject.name }}</h2>
          <p class="text-muted">{{ subject.description }}</p>
          <div class="d-flex gap-2 mt-2">
            <button class="btn btn-outline-primary" @click="editSubject">
              <i class="bi bi-pencil-square me-1"></i> Edit
            </button>
            <button class="btn btn-outline-danger" @click="deleteSubject">
              <i class="bi bi-trash me-1"></i> Delete
            </button>
          </div>
        </div>

        <!-- Create Chapter -->
        <div class="mb-4">
          <button
            class="btn btn-success"
            @click="showCreateChapterForm = !showCreateChapterForm"
          >
            <i class="bi bi-plus-circle me-1"></i> Create Chapter
          </button>
        </div>

        <!-- Create Chapter Form -->
        <div v-if="showCreateChapterForm" class="card p-3 mb-4 shadow-sm">
          <h5 class="mb-3">New Chapter Details</h5>
          <div class="row g-3">
            <div class="col-md-4">
              <input
                v-model="newChapter.name"
                class="form-control"
                placeholder="Chapter Name"
              />
            </div>
            <div class="col-md-4">
              <input
                v-model="newChapter.description"
                class="form-control"
                placeholder="Description"
              />
            </div>
            <div class="col-md-4">
              <select v-model="newChapter.difficulty_level" class="form-select">
                <option disabled value="">Difficulty Level</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
          </div>
          <div class="mt-3">
            <button class="btn btn-primary me-2" @click="createChapter">
              Submit
            </button>
            <button
              class="btn btn-secondary"
              @click="showCreateChapterForm = false"
            >
              Cancel
            </button>
          </div>
        </div>

        <!-- Chapter List Table -->
        <div class="card shadow-sm">
          <div class="card-header bg-primary text-white fw-semibold">
            Chapters
          </div>
          <div class="card-body p-0">
            <table class="table table-hover m-0">
              <thead class="table-light">
                <tr>
                  <th>Chapter Name</th>
                  <th>Description</th>
                  <th>Difficulty level</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="chapter in chapters" :key="chapter.chapter_id">
                  <td>{{ chapter.name }}</td>
                  <td>{{ chapter.description }}</td>
                  <td class="text-capitalize">{{ chapter.difficulty_level }}</td>
                  <td>
                    <button
                      @click="viewQuiz(chapter.chapter_id)"
                      class="btn btn-sm btn-info me-2"
                    >
                      View Quiz
                    </button>
                    <button
                      @click="editChapter(chapter.chapter_id)"
                      class="btn btn-sm btn-warning me-2"
                    >
                      Edit
                    </button>
                    <button
                      @click="deleteChapter(chapter.chapter_id)"
                      class="btn btn-sm btn-danger"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
                <tr v-if="chapters.length === 0">
                  <td colspan="4" class="text-center text-muted py-3">
                    No chapters yet
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!-- container -->
    </div>
    <!-- flex-grow-1 -->
  </div>
  <!-- d-flex -->
</template>

<script>
import axios from "axios";
import Navbar from "@/components/navbar.vue";
import Sidebar from "@/components/sidebar.vue";

export default {
  name: "SubjectDetail",
  components: {
    Sidebar,
    Navbar,
  },
  data() {
    return {
      subject: {},
      chapters: [],
      showCreateChapterForm: false,
      newChapter: {
        name: "",
        description: "",
        difficulty_level: "",
      },
    };
  },
  methods: {
    async fetchSubjectDetails() {
      const subjectId = this.$route.params.subjectId;
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          `http://localhost:5000/admin/subject/${subjectId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
        this.subject = response.data.subject;
        this.chapters = response.data.chapters;
      } catch (error) {
        console.error("Failed to fetch subject details:", error);
      }
    },

    async createChapter() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch(`http://localhost:5000/admin/chapters`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            subject_id: this.$route.params.subjectId,  // fixed this line too
            name: this.newChapter.name,
            description: this.newChapter.description,
            difficulty_level: this.newChapter.difficulty_level,
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to create chapter");
        }

        const data = await response.json();
        this.chapters.push(data);
        this.showCreateChapterForm = false;
        this.newChapter = { name: "", description: "", difficulty_level: "" };
      } catch (error) {
        console.error(error);
        alert("Error creating chapter");
      }
    },

    editSubject() {
      // Navigate to edit subject page
    },
    deleteSubject() {
      // Delete the subject
    },
    viewQuiz(chapterId) {
      // Redirect to quiz view for this chapter
    },
    editChapter(chapterId) {
      // Navigate to edit chapter page
    },
    deleteChapter(chapterId) {
      // Delete chapter logic
    },
  },

  mounted() {
    this.fetchSubjectDetails();
  },
};
</script>


<style scoped>
/* Add styles as needed */
</style>
