<template>
  <div class="d-flex vh-100 overflow-hidden position-relative">
    <!-- Sidebar -->
    <Sidebar
      class="bg-dark text-white position-fixed h-100"
      style="width: 175px"
    />

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column" style="margin-left: 175px">
      <!-- Navbar -->
      <Navbar class="bg-white shadow-sm position-sticky top-0 z-3" />

      <div
        v-if="showFlash"
        :class="`alert alert-${flashType} alert-dismissible fade show`"
        role="alert"
      >
        {{ flashMessage }}
        <button
          type="button"
          class="btn-close"
          @click="showFlash = false"
        ></button>
      </div>

      <!-- Scrollable content -->
      <div class="flex-grow-1 overflow-auto px-4 py-4">
        <h3 class="fw-bold">❓ Questions for {{ quizName }}</h3>

        <!-- Create Button -->
        <div class="row mb-3">
          <div class="col-auto">
            <button class="btn btn-success" @click="showCreateForm = true">
              + Add Question
            </button>
          </div>
        </div>

        <!-- Create Form -->
        <div v-if="showCreateForm" class="card shadow mb-4">
          <div class="card-header bg-light fw-semibold">
            Create New Question
          </div>
          <div class="card-body">
            <form @submit.prevent="submitQuestion">
              <div class="mb-3">
                <label class="form-label">Question Statement</label>
                <textarea
                  v-model="questionForm.question_statement"
                  class="form-control"
                  required
                ></textarea>
              </div>

              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Option 1</label>
                  <input
                    v-model="questionForm.option1"
                    class="form-control"
                    required
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Option 2</label>
                  <input
                    v-model="questionForm.option2"
                    class="form-control"
                    required
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Option 3</label>
                  <input
                    v-model="questionForm.option3"
                    class="form-control"
                    required
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Option 4</label>
                  <input
                    v-model="questionForm.option4"
                    class="form-control"
                    required
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label">
                    Correct Option (option1/option2/option3/option4)
                  </label>
                  <select
                    v-model="questionForm.correct_option"
                    class="form-select"
                    required
                  >
                    <option value="option1">Option 1</option>
                    <option value="option2">Option 2</option>
                    <option value="option3">Option 3</option>
                    <option value="option4">Option 4</option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Difficulty (optional)</label>
                  <input
                    v-model="questionForm.difficulty"
                    class="form-control"
                    placeholder="Easy, Medium, Hard"
                  />
                </div>
                <div class="col-md-12">
                  <label class="form-label">Explanation (optional)</label>
                  <textarea
                    v-model="questionForm.explanation"
                    class="form-control"
                    rows="3"
                  ></textarea>
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

        <!-- Questions Table -->
        <div v-if="questions.length" class="card shadow">
          <div class="card-body p-0">
            <table class="table table-hover table-bordered table-striped mb-0">
              <thead class="table-dark text-center align-middle">
                <tr>
                  <th>Question Statement</th>
                  <th>Options</th>
                  <th>Correct</th>
                  <th>Difficulty</th>
                  <th>Explanation</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="question in questions"
                  :key="question.question_id"
                  class="text-center align-middle"
                >
                  <td class="text-start">{{ question.question_statement }}</td>
                  <td class="text-start">
                    <ul class="list-unstyled mb-0">
                      <li><strong>Option 1:</strong> {{ question.option1 }}</li>
                      <li><strong>Option 2:</strong> {{ question.option2 }}</li>
                      <li><strong>Option 3:</strong> {{ question.option3 }}</li>
                      <li><strong>Option 4:</strong> {{ question.option4 }}</li>
                    </ul>
                  </td>
                  <td>{{ question.correct_option }}</td>
                  <td>{{ question.difficulty || "-" }}</td>
                  <td class="text-start">{{ question.explanation || "-" }}</td>
                  <td>
                    <div class="btn-group">
                      <button
                        class="btn btn-sm btn-primary"
                        @click="openEditModal(question)"
                      >
                        Edit
                      </button>
                      <button
                        class="btn btn-sm btn-danger"
                        @click="deleteQuestion(question.question_id)"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="alert alert-info mt-4">
          No questions added yet for this quiz.
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <EditQuestionModal
      v-if="showEditModal"
      :question="editQuestion"
      @close="showEditModal = false"
      @updated="fetchQuestions"
      @flash="handleFlash"
    />
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar.vue";
import Navbar from "@/components/Navbar.vue";
import EditQuestionModal from "@/components/EditQuestionModal.vue";
import axios from "axios";

export default {
  name: "QuestionList",
  components: { Sidebar, Navbar, EditQuestionModal },
  props: ["quizId", "quizName"],
  data() {
    return {
      questions: [],
      showCreateForm: false,
      showEditModal: false,
      editQuestion: null,
      questionForm: {
        question_statement: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_option: "",
        difficulty: "",
        explanation: "",
      },
      flashMessage: "",
      flashType: "", // 'success', 'danger', 'info', etc.
      showFlash: false,
    };
  },
  methods: {
    handleFlash({ message, type }) {
      this.flashMessage = message;
      this.flashType = type;
      this.showFlash = true;
      setTimeout(() => {
        this.showFlash = false;
      }, 3000);
    },
    async fetchQuestions() {
      try {
        const response = await axios.get(
          `http://localhost:5000/admin/quizzes/${this.quizId}/questions`
        );
        console.log("Fetched questions:", response.data); // Add this for debugging
        this.questions = Array.isArray(response.data)
          ? response.data
          : response.data.questions || [];
      } catch (error) {
        console.error("Failed to fetch questions.", error);
      }
    },
    async submitQuestion() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.post(
          `http://localhost:5000/admin/quizzes/${this.quizId}/questions`,
          JSON.stringify(this.questionForm),
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
        this.showCreateForm = false;
        this.resetForm();

        // Show success flash message
        this.flashMessage =
          response.data.message || "Question created successfully!";
        this.flashType = "success";
        this.showFlash = true;
        // Refresh the question list
        await this.fetchQuestions();

        setTimeout(() => {
          this.showFlash = false;
        }, 3000);
      } catch (error) {
        this.flashMessage = "Failed to create question.";
        this.flashType = "danger";
        this.showFlash = true;
        setTimeout(() => {
          this.showFlash = false;
        }, 3000);
        console.error(
          "Failed to create question:",
          error.response?.data || error.message
        );
      }
    },

    resetForm() {
      this.questionForm = {
        question_statement: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_option: "",
        difficulty: "",
        explanation: "",
      };
    },

    async deleteQuestion(questionId) {
      if (!confirm("Are you sure you want to delete this question?")) return;
      try {
        const token = localStorage.getItem("access_token");
        await axios.delete(
          `http://localhost:5000/admin/questions/${questionId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        // Remove the deleted question from the local list
        this.questions = this.questions.filter(
          (q) => q.question_id !== questionId
        );
        this.flashMessage = "Question deleted successfully!";
        this.flashType = "success";
        this.showFlash = true;
        setTimeout(() => {
          this.showFlash = false;
        }, 3000);
      } catch (error) {
        this.flashMessage = "Failed to delete question.";
        this.flashType = "danger";
        this.showFlash = true;
        setTimeout(() => {
          this.showFlash = false;
        }, 3000);
        console.error(
          "Failed to delete question:",
          error.response?.data || error.message
        );
      }
    },
    openEditModal(question) {
      this.editQuestion = { ...question };
      this.showEditModal = true;
    },
  },
  mounted() {
    this.fetchQuestions();
  },
};
</script>

<style scoped>
.table th,
.table td {
  vertical-align: middle;
}
</style>
