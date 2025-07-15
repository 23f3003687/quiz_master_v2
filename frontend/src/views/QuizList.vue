<template>
  <div class="d-flex vh-100 ">
    <!-- Sidebar on the left -->
    <Sidebar class="bg-dark text-white" />

    <!-- Main content on the right -->
    <div class="flex-grow-1 d-flex flex-column">
      <!-- Navbar at the top -->
      <Navbar class="bg-white shadow-sm" />

      <!-- Flash Message -->
      <div
        v-if="showFlash"
        :class="`alert alert-${flashType} alert-dismissible fade show position-absolute top-0 start-50 translate-middle-x mt-3`"
        role="alert"
        style="z-index: 1050; min-width: 300px"
      >
        {{ flashMessage }}
        <button
          type="button"
          class="btn-close"
          aria-label="Close"
          @click="showFlash = false"
        ></button>
      </div>

      <div class="container mt-4">
        <div class="container mt-2 pt-5 flex-grow-1 overflow-auto">
          <h3 class="fw-bold">📋 Quizzes for {{ chapterName }}</h3>

          <!-- Align Create Quiz button to the left -->
          <div class="row mb-4">
            <div class="col-auto">
              <button class="btn btn-success" @click="showCreateForm = true">
                + Create Quiz
              </button>
            </div>
          </div>
        </div>

        <div v-if="loading" class="spinner-border text-primary"></div>
        <div v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </div>

        <!-- Create Quiz Form -->
        <div v-if="showCreateForm" class="card shadow mb-4">
          <div class="card-header bg-light fw-semibold">Create New Quiz</div>
          <div class="card-body">
            <form @submit.prevent="submitQuiz">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Name</label>
                  <input
                    v-model="Quiz.name"
                    type="text"
                    class="form-control"
                    required
                  />
                </div>
                <div class="col-md-4">
                  <label class="form-label">Duration (minutes)</label>
                  <input
                    v-model="Quiz.time_duration"
                    type="text"
                    class="form-control"
                    required
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Start Time</label>
                  <input
                    v-model="Quiz.start_datetime"
                    type="datetime-local"
                    class="form-control"
                    required
                  />
                </div>
    
                <div class="col-md-6">
                  <label class="form-label">Remarks</label>
                  <input
                    v-model="Quiz.remarks"
                    type="text"
                    class="form-control"
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Tags</label>
                  <input v-model="Quiz.tags" type="text" class="form-control" />
                </div>
              </div>
              <div class="mt-3">
                <button type="submit" class="btn btn-primary btn-sm">
                  Submit
                </button>
                <button
                  type="button"
                  class="btn btn-secondary btn-sm ms-2"
                  @click="cancelCreate"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Quizzes Table -->
        <div v-if="quizzes.length" class="card shadow">
          <div class="card-body p-0">
            <table class="table table-hover table-bordered table-striped mb-0">
              <thead class="table-dark text-center align-middle">
                <tr>
                  <th>Name</th>
                  <th>Duration</th>
                  <th>Start Time</th>
                  <th>Total Marks</th>
                  <th>No. of Questions</th>
                  <th>Remarks</th>
                  <th>Tags</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="quiz in quizzes"
                  :key="quiz.quiz_id"
                  class="text-center align-middle"
                >
                  <td>{{ quiz.name }}</td>
                  <td>{{ quiz.time_duration }}</td>
                  <td>{{ formatDateTime(quiz.start_datetime) }}</td>
                  <td>{{ quiz.total_marks }}</td>
                  <td>{{ quiz.num_questions }}</td>
                  <td>{{ quiz.remarks }}</td>
                  <td>
                    <span
                      v-for="tag in quiz.tags.split(',')"
                      :key="tag"
                      class="badge bg-warning me-1"
                    >
                      {{ tag.trim() }}
                    </span>
                  </td>
                  <td>
                    <div class="btn-group">
                      <button
                        class="btn btn-sm btn-primary"
                        @click="openEditModal(quiz)"
                      >
                        Edit
                      </button>
                      <button
                        class="btn btn-sm btn-danger"
                        @click="deleteQuiz(quiz.quiz_id)"
                      >
                        Delete
                      </button>
                      <button
                        class="btn btn-sm btn-info text-white"
                        @click="viewQuestions(quiz.quiz_id)"
                      >
                        View Questions
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Show message if no quizzes -->
        <div v-else class="alert alert-info mt-4">
          No quizzes added yet for this chapter.
        </div>
      </div>
    </div>
    <EditQuizModal
      v-if="showEditModal"
      :quiz="editQuiz"
      @close="showEditModal = false"
      @updated="fetchQuizzes"
      @flash="handleFlash"
    />
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "@/components/navbar.vue";
import Sidebar from "@/components/sidebar.vue";
import EditQuizModal from "@/components/EditQuizModal.vue";
export default {
  components: {
    Sidebar,
    Navbar,
    EditQuizModal,
  },
  props: {
    chapterId: Number,
    chapterName: String,
  },
  data() {
    return {
      quizzes: [],
      loading: false,
      errorMessage: "",
      showCreateForm: false,
      Quiz: {
        name: "",
        time_duration: "",
        start_datetime: "",
        remarks: "",
        tags: "",
      },
      editQuiz: null,
      showEditModal: false,
      selectedQuizQuestions: [],
      selectedQuizId: null,
      showQuestionsModal: false,
      flashMessage: "",
      flashType: "", // 'success' or 'danger'
      showFlash: false,
    };
  },
  watch: {
    chapterId: {
      immediate: true,
      handler() {
        this.fetchQuizzes();
      },
    },
  },
  methods: {
    formatDateTime(datetimeStr) {
      if (!datetimeStr) return "-";
      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(datetimeStr).toLocaleString(undefined, options);
    },

    handleFlash({ message, type }) {
      this.flashMessage = message;
      this.flashType = type;
      this.showFlash = false; // reset first
      this.$nextTick(() => {
        this.showFlash = true;
        setTimeout(() => (this.showFlash = false), 3000);
      });
    },

    async fetchQuizzes() {
      if (!this.chapterId) return;

      this.loading = true;
      this.errorMessage = "";
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          `http://localhost:5000/admin/chapters/${this.chapterId}/quizzes`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.quizzes = response.data;
      } catch (err) {
        this.errorMessage = "Failed to load quizzes";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    cancelCreate() {
      this.showCreateForm = false;
      // Reset form
      this.Quiz = {
        name: "",
        time_duration: "",
        remarks: "",
        tags: "",
      };
    },
    async submitQuiz() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.post(
          `http://localhost:5000/admin/chapters/${this.chapterId}/quizzes`,
          JSON.stringify(this.Quiz), // 🔥 Force raw JSON
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json", // Required when using stringify
            },
          }
        );
        this.quizzes.push(response.data);
        this.cancelCreate();
        // Show success flash message
        this.flashMessage = "Quiz created successfully!";
        this.flashType = "success";
        this.showFlash = true;
        setTimeout(() => (this.showFlash = false), 3000);
      } catch (err) {
        // Show error flash message
        this.flashMessage = "Failed to create quiz.";
        this.flashType = "danger";
        this.showFlash = true;
        setTimeout(() => (this.showFlash = false), 3000);
        console.error(err);
      }
    },
    openEditModal(quiz) {
      this.editQuiz = { ...quiz }; // Clone to avoid 2-way binding issues
      this.showEditModal = true;
    },

    async deleteQuiz(quizId) {
      if (!confirm("Are you sure you want to delete this quiz?")) return;
      try {
        const token = localStorage.getItem("access_token");
        await axios.delete(`http://localhost:5000/admin/quizzes/${quizId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.quizzes = this.quizzes.filter((q) => q.quiz_id !== quizId);

        this.flashMessage = "Quiz deleted successfully!";
        this.flashType = "success";
        this.showFlash = false;
        this.$nextTick(() => {
          this.showFlash = true;
          setTimeout(() => (this.showFlash = false), 3000);
        });
      } catch (err) {
        this.flashMessage = "Failed to delete quiz.";
        this.flashType = "danger";
        this.showFlash = false;
        this.$nextTick(() => {
          this.showFlash = true;
          setTimeout(() => (this.showFlash = false), 3000);
        });
        console.error(err);
      }
    },

    viewQuestions(quizId) {
      this.$router.push({ name: "QuizQuestions", params: { quizId } });
    },
  },
};
</script>
