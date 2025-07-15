<template>
  <div class="d-flex min-vh-100">
    <!-- Sidebar -->
    <UserSidebar class="bg-dark text-white" />

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column" style="margin-left: 175px">
      <!-- Navbar -->
      <UserNavbar class="bg-white shadow-sm" />
      <div class="container mt-4">
        <h3 class="mb-4 text-success">🎉 Quiz submitted successfully!</h3>
        <div class="text-muted">
          <strong>⏱ Time Taken:</strong> {{ timeTaken }}
        </div>
        <div v-if="remarks" class="alert alert-info">
          <strong>💬</strong> {{ remarks }}
        </div>

        <div class="row mb-4">
          <div class="col-md-3" v-for="card in scoreCards" :key="card.label">
            <div class="card text-center shadow">
              <div class="card-body">
                <h5 class="card-title">{{ card.label }}</h5>
                <p
                  class="card-text fw-bold"
                  :class="{
                    'text-success':
                      card.label === 'Status' && card.value === 'PASSED',
                    'text-danger':
                      card.label === 'Status' && card.value === 'FAILED',
                  }"
                >
                  {{ card.value }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <h4 class="mb-3">📋 Question Review</h4>
        <div
          v-for="(q, index) in questions"
          :key="index"
          class="card mb-3 shadow-sm"
        >
          <div class="card-body">
            <h5 class="card-title">
              Q{{ index + 1 }}: {{ q.question_statement }}
            </h5>
            <p>
              <strong>Selected Option:</strong> {{ q.selected_option }} <br />
              <strong>Correct Option:</strong> {{ q.correct_option }}
            </p>
            <p>
              <strong>Status:</strong>
              <span
                :class="
                  q.selected_option === 'skipped'
                    ? 'text-warning'
                    : q.is_correct
                    ? 'text-success'
                    : 'text-danger'
                "
              >
                {{
                  q.selected_option === "skipped"
                    ? "Skipped ⚠️"
                    : q.is_correct
                    ? "Correct ✅"
                    : "Wrong ❌"
                }}
              </span>
            </p>

            <p>
              <strong>Difficulty:</strong> {{ q.difficulty || "Not specified" }}
            </p>
            <p>
              <strong>Explanation:</strong>
              {{ q.explanation || "No explanation provided." }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";
import UserSidebar from "@/components/UserSidebar.vue";
import UserNavbar from "@/components/UserNavbar.vue";

export default {
  name: "ScoreCard",
  components: {
    UserSidebar,
    UserNavbar,
  },
  setup() {
    const route = useRoute();
    const scoreId = route.params.score_id;
    const timeTaken = ref("");
    const scoreCards = ref([]);
    const questions = ref([]);
    const remarks = ref("");

    onMounted(async () => {
      const token = localStorage.getItem("access_token");
      try {
        const res = await axios.get(
          `http://localhost:5000/user/score/${scoreId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = res.data;
        const total = data.total_questions;
        const accuracy =
          total > 0
            ? ((data.correct_answers / total) * 100).toFixed(0) + "%"
            : "N/A";

        remarks.value = data.remarks;
        timeTaken.value = data.time_taken || "N/A";

        scoreCards.value = [
          {
            label: "Total Score",
            value: `${data.total_score}/${data.quiz_total_marks}`,
          },
          { label: "Accuracy", value: accuracy },
          {
            label: "Attempted",
            value: `${data.attempted_questions}/${data.total_questions}`,
          },
          { label: "Status", value: data.status },
        ];

        questions.value = data.questions;
      } catch (err) {
        console.error("Error fetching scorecard:", err);
      }
    });

    return {
      scoreCards,
      questions,
      remarks,
      timeTaken,
    };
  },
};
</script>
