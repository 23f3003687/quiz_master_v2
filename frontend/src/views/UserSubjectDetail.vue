<template>
  <div class="d-flex min-vh-100">
    <!-- Sidebar -->
    <UserSidebar class="bg-dark text-white" />

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column" style="margin-left: 175px">
      <!-- Navbar -->
      <UserNavbar class="bg-white shadow-sm mb-3" />

      <!-- Page Content -->
      <div class="container pt-5 mt-4">
        <h3>Quizzes For {{ subject.name }}</h3>
        <p class="text-muted">{{ subject.description }}</p>

        <div v-if="quizzes.length === 0" class="mt-4">
          <p>No quizzes available for this subject.</p>
        </div>

        <div v-else class="mt-4">
          <div class="row">
            <div
              class="col-md-4 mb-4"
              v-for="quiz in quizzes"
              :key="quiz.quiz_id"
            >
              <div
                class="card h-100 shadow-lg p-3 border-start transition hover-card border-3"
              >
                <div class="card-body">
                  <h5 class="card-title">{{ quiz.name }}</h5>
                  <h6 class="card-subtitle text-muted mb-2">
                    Chapter: {{ quiz.chapter.name }}
                  </h6>
                  <p>
                    <strong>Description:</strong> {{ quiz.chapter.description }}
                  </p>
                  <!-- Difficulty with color-coded badge -->
                  <p>
                    <strong>Difficulty: </strong>
                    <span
                      class="badge"
                      :class="{
                        'bg-success': quiz.chapter.difficulty_level === 'easy',
                        'bg-warning text-dark':
                          quiz.chapter.difficulty_level === 'medium',
                        'bg-danger': quiz.chapter.difficulty_level === 'hard',
                      }"
                    >
                      {{ quiz.chapter.difficulty_level }}
                    </span>
                  </p>
                  <hr />
                  <p>
                    <strong>Duration:</strong> {{ quiz.time_duration }} mins
                  </p>
                  <p>
                    <strong>Start Date & Time:</strong>
                    {{ formatDate(quiz.start_datetime) }}
                  </p>

                  <p><strong>Total Marks:</strong> {{ quiz.total_marks }}</p>
                  <p>
                    <strong>No. of Questions:</strong> {{ quiz.num_questions }}
                  </p>
                  <p><strong>Remarks:</strong> {{ quiz.remarks }}</p>
                  <!-- Tags as badges -->
                  <p>
                    <strong>Tags: </strong>
                    <span
                      class="badge bg-primary me-1"
                      v-for="(tag, index) in quiz.tags.split(',')"
                      :key="index"
                    >
                      {{ quiz.tags }}
                    </span>
                  </p>
                  <!-- Start Quiz button -->
                  <div class="mt-3 text-end">
                    <button
                      class="btn btn-success mt-3"
                      @click="confirmStartQuiz(quiz)"
                    >
                      Start Quiz
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Start Quiz Confirmation Modal -->
  <div class="modal fade" id="startQuizModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content border-danger">
        <div class="modal-header bg-danger text-white">
          <h5 class="modal-title">Warning</h5>
        </div>
        <div class="modal-body">
          <p>
            ⏰
            <strong>The timer will start as soon as you begin the quiz.</strong>
          </p>
          <p>
            Try to attempt all questions. You won't be able to pause or restart.
          </p>
        </div>
        <div class="modal-footer">
          <button
            class="btn btn-danger"
            data-bs-dismiss="modal"
            @click="startQuizConfirmed"
          >
            OK, Got it!
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UserSidebar from "@/components/UserSidebar.vue";
import UserNavbar from "@/components/UserNavbar.vue";
import { Modal } from "bootstrap";

export default {
  name: "UserSubjectDetail",
  components: {
    UserSidebar,
    UserNavbar,
  },
  props: ["subjectId"],
  data() {
    return {
      subject: {},
      quizzes: [],
      selectedQuiz: null,
    };
  },
  methods: {
    confirmStartQuiz(quiz) {
      this.selectedQuiz = quiz;
      const modal = new Modal(document.getElementById("startQuizModal"));
      modal.show();
    },
    startQuizConfirmed() {
      // Navigate to quiz attempt page with quizId
      this.$router.push({
        name: "QuizAttempt",
        params: { quizId: this.selectedQuiz.quiz_id },
        query: {subjectId: this.subjectId },
      });
    },

    async fetchSubject() {
      try {
        const res = await axios.get("http://localhost:5000/user/subjects", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        this.subject =
          res.data.subjects.find((s) => s.subject_id == this.subjectId) || {};
      } catch (err) {
        console.error("Error fetching subject:", err);
      }
    },
    async fetchQuizzes() {
      try {
        const res = await axios.get(
          `http://localhost:5000/user/subject/${this.subjectId}/quizzes`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        this.quizzes = res.data;
      } catch (err) {
        console.error("Error fetching quizzes:", err);
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "-";
      const d = new Date(dateStr);
      return d.toLocaleString([], {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
  async mounted() {
    await this.fetchSubject();
    await this.fetchQuizzes();
  },
};
</script>

<style scoped>
.card {
  border-left: 6px solid #007bff;
  padding-left: 15px;
}
.card {
  transition: transform 0.2s;
}
.card:hover {
  transform: scale(1.02);
}

.hover-card:hover {
  background-color: rgb(243, 240, 240); /* light hover color */
  box-shadow: 0 4px 12px rgb(117, 25, 25); /* stronger shadow */
}
</style>
