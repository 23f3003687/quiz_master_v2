<template>
  <div class="d-flex vh-100">
    <!-- Sidebar -->
    <UserSidebar class="bg-dark text-white" />

    <!-- Main content -->
    <div class="flex-grow-1 d-flex flex-column" style="margin-left: 175px">
      <!-- Navbar -->
      <UserNavbar class="bg-white shadow-sm" />

      <!-- Quiz Content -->
      <div v-if="!hasError" class="container mt-4 position-relative">
        <!-- Timer -->
        <div class="position-absolute top-0 end-0 mt-2 me-3">
          <span class="badge bg-danger fs-6 px-3 py-2">
            ⏰ {{ formattedTime }}
          </span>
        </div>

        <!-- Quiz Title -->
        <h4 class="mb-4">Quiz: {{ quiz.name }}</h4>

        <!-- Question Card -->
        <div class="card shadow-lg">
          <div class="card-body">
            <h5 class="card-title">Question {{ currentIndex + 1 }}</h5>
            <p class="card-text fs-5">
              {{ currentQuestion.question_statement }}
            </p>

            <!-- Options -->
            <div
              class="mt-3"
              v-if="currentQuestion && currentQuestion.question_id"
            >
              <div
                class="form-check mb-2"
                v-for="(optionValue, optionKey) in getOptions(currentQuestion)"
                :key="optionKey"
              >
                <input
                  class="form-check-input"
                  type="radio"
                  :id="optionKey"
                  :value="optionKey"
                  v-model="selectedAnswers[currentQuestion.question_id]"
                  :name="'options_' + currentQuestion.question_id"
                />
                <label class="form-check-label" :for="optionKey">
                  {{ optionValue }}
                </label>
              </div>
            </div>

            <!-- Navigation Buttons -->
            <div class="mt-4 d-flex justify-content-between">
              <button
                class="btn btn-outline-secondary"
                :disabled="currentIndex === 0"
                @click="prevQuestion"
              >
                ← Previous
              </button>
              <button class="btn btn-primary" @click="nextQuestion">
                {{
                  currentIndex === questions.length - 1 ? "Submit" : "Next →"
                }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserSidebar from "@/components/UserSidebar.vue";
import UserNavbar from "@/components/UserNavbar.vue";
import axios from "axios";

export default {
  name: "QuizAttempt",
  components: {
    UserSidebar,
    UserNavbar,
  },
  props: ["quizId", "subjectId"],
  data() {
    return {
      quiz: {},
      questions: [],
      currentIndex: 0,
      selectedAnswers: {},
      timer: null,
      timeLeft: 600, // default: 10 minutes
      hasError: false,
      errorMessage: "",
      localSubjectId: null,
    };
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentIndex] || {};
    },
    formattedTime() {
      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;
      return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    },
  },
  mounted() {
    this.fetchQuizData();
    this.startTimer();
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  methods: {
    getOptions(question) {
      if (!question) return {};
      return Object.fromEntries(
        Object.entries({
          option1: question.option1,
          option2: question.option2,
          option3: question.option3,
          option4: question.option4,
        }).filter(([_, value]) => value && value.trim() !== "")
      );
    },

    fetchQuizData() {
      axios
        .get(`http://localhost:5000/user/quiz/${this.quizId}/attempt`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((res) => {
          this.quiz = res.data.quiz;
          this.questions = res.data.questions;
          this.localSubjectId = res.data.quiz.subject_id;
          this.timeLeft = this.quiz.time_duration * 60; // minutes to seconds
        })
        .catch((err) => {
          this.hasError = true;
          if (err.response && err.response.status === 403) {
            this.errorMessage = err.response.data.error;
            alert(this.errorMessage);
            const sid =
              this.localSubjectId ||
              this.subjectId ||
              this.$route.query.subjectId;
            this.$router.push(`/user/subject/${sid}`);
          } else {
            this.errorMessage = "Something went wrong while fetching the quiz.";
            alert(this.errorMessage);
          }
        });
    },

    startTimer() {
      this.timer = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
        } else {
          clearInterval(this.timer);
          alert("Time is up! Submitting the quiz...");
          this.submitQuiz();
        }
      }, 1000);
    },
    nextQuestion() {
      if (this.currentIndex < this.questions.length - 1) {
        this.currentIndex++;
      } else {
        this.submitQuiz();
      }
    },
    prevQuestion() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
    },
    submitQuiz() {
      const secondsTaken = this.quiz.time_duration * 60 - this.timeLeft;
      const minutes = Math.floor(secondsTaken / 60);
      const seconds = secondsTaken % 60;
      const formattedTime = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;

      const payload = {
        quiz_id: this.quizId,
        answers: Object.entries(this.selectedAnswers).map(
          ([question_id, selected_option]) => ({
            question_id: parseInt(question_id),
            selected_option,
          })
        ),
        time_taken: formattedTime,
      };

      axios
        .post(
          `http://localhost:5000/user/submit-quiz/${this.quizId}`,
          payload,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        )
        .then((res) => {
          const score_id = res.data.score_id;
          this.$router.push(`/user/scorecard/${score_id}`);
        })
        .catch((err) => {
          console.error("Error submitting quiz:", err);
          alert("Error submitting quiz. Please try again.");
        });
    },
  },
};
</script>

<style scoped>
.card {
  max-width: 800px;
  margin: 0 auto;
}
.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}
</style>
