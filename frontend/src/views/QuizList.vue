<template>
  <div>
    <h3>Quizzes</h3>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <div></div>
      <!-- empty placeholder for left -->
      <button class="btn btn-success" @click="showCreateForm = true">
        Create Quiz
      </button>
    </div>

    <div v-if="loading" class="spinner-border"></div>
    <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

    <!-- Create Quiz Form -->
    <div v-if="showCreateForm" class="card mb-4 p-3 border">
      <h5>Create New Quiz</h5>
      <form @submit.prevent="submitQuiz">
        <div class="mb-2">
          <label class="form-label">Name</label>
          <input
            v-model="Quiz.name"
            type="text"
            class="form-control"
            required
          />
        </div>
        <div class="mb-2">
          <label class="form-label">Date of Quiz</label>
          <input
            v-model="Quiz.date_of_quiz"
            type="date"
            class="form-control"
            required
          />
        </div>
        <div class="mb-2">
          <label class="form-label">Duration (minutes)</label>
          <input
            v-model="Quiz.time_duration"
            type="text"
            class="form-control"
            required
          />
        </div>
        <div class="mb-2">
          <label class="form-label">Total Marks</label>
          <input
            v-model.number="Quiz.total_marks"
            type="number"
            class="form-control"
            required
          />
        </div>
        <div class="mb-2">
          <label class="form-label">Questions</label>
          <input
            v-model="Quiz.num_questions"
            type="text"
            class="form-control"
            required
          />
        </div>
        <div class="mb-2">
          <label class="form-label">Remarks</label>
          <input v-model="Quiz.remarks" type="text" class="form-control" />
        </div>
        <div class="mb-2">
          <label class="form-label">Tags (comma separated)</label>
          <input v-model="Quiz.tags" type="text" class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary btn-sm">Submit</button>
        <button
          type="button"
          class="btn btn-secondary btn-sm ms-2"
          @click="cancelCreate"
        >
          Cancel
        </button>
      </form>
    </div>

    <!-- Quizzes Table -->
    <table v-if="quizzes.length" class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Date</th>
          <th>Duration</th>
          <th>Total Marks</th>
          <th>Questions</th>
          <th>Remarks</th>
          <th>Tags</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="quiz in quizzes" :key="quiz.quiz_id">
          <td>{{ quiz.name }}</td>
          <td>{{ quiz.date_of_quiz }}</td>
          <td>{{ quiz.time_duration }}</td>
          <td>{{ quiz.total_marks }}</td>
          <td>{{ quiz.num_questions }}</td>
          <td>{{ quiz.remarks }}</td>
          <td>{{ quiz.tags }}</td>
          <td>
            <button class="btn btn-primary btn-sm" @click="$emit('edit', quiz)">
              Edit
            </button>
            <button
              class="btn btn-danger btn-sm"
              @click="$emit('delete', quiz.quiz_id)"
            >
              Delete
            </button>
            <button
              class="btn btn-info btn-sm"
              @click="$emit('view-questions', quiz.quiz_id)"
            >
              View Questions
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Show message if no quizzes -->
    <div v-else class="alert alert-info">
      No quizzes added yet for this chapter.
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    chapterId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      quizzes: [],
      loading: false,
      errorMessage: "",
      showCreateForm: false,
      Quiz: {
        name: "",
        date_of_quiz: "",
        time_duration: "",
        total_marks: null,
        num_questions: "",
        remarks: "",
        tags: "",
      },
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
        date_of_quiz: "",
        time_duration: "",
        total_marks: null,
        num_questions: "",
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
      } catch (err) {
        alert("Failed to create quiz.");
        console.error(err);
      }
    },
  },
};
</script>
