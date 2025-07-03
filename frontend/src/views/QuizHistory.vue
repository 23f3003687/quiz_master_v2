<template>
  <div class="d-flex min-vh-100">
    <!-- Sidebar -->
    <UserSidebar class="bg-dark text-white" />

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column" style="margin-left: 175px">
      <!-- Navbar -->
      <UserNavbar class="bg-white shadow-sm" />

      <div class="container mt-4">
        <h3 class="mb-4">📘 Quiz History</h3>

        <!-- Export Button -->
        <div class="mb-3">
          <button
            class="btn btn-outline-success"
            @click="exportQuizHistory"
            :disabled="exporting"
          >
            <span v-if="exporting">📤 Exporting...</span>
            <span v-else>📥 Export Quiz History</span>
          </button>
        </div>

        <div v-if="history.length === 0" class="alert alert-info">
          No quiz attempts found.
        </div>

        <table v-else class="table table-striped shadow-sm">
          <thead class="table-dark">
            <tr>
              <th>Sr.no.</th>
              <th>Quiz Name</th>
              <th>Date</th>
              <th>Score</th>
              <th>Accuracy</th>
              <th>Status</th>
              <th>View Scorecard</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in history" :key="item.score_id">
              <td>{{ index + 1 }}</td>
              <td>{{ item.quiz_name }}</td>
              <td>{{ item.time_stamp_of_attempt }}</td>
              <td>{{ item.score }}</td>
              <td>{{ item.accuracy }}</td>
              <td>
                <span
                  :class="
                    item.status === 'PASSED'
                      ? 'text-success fw-bold'
                      : 'text-danger fw-bold'
                  "
                >
                  {{ item.status }}
                </span>
              </td>
              <td>
                <router-link
                  class="btn btn-sm btn-outline-primary"
                  :to="`/user/scorecard/${item.score_id}`"
                >
                  View
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import UserSidebar from "@/components/UserSidebar.vue";
import UserNavbar from "@/components/UserNavbar.vue";

export default {
  name: "QuizHistory",
  components: {
    UserSidebar,
    UserNavbar,
  },
  setup() {
    const history = ref([]);
    const exporting = ref(false);

    onMounted(async () => {
      const token = localStorage.getItem("access_token");
      try {
        const res = await axios.get(
          "http://localhost:5000/user/score/history",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        history.value = res.data;
      } catch (err) {
        console.error("Error loading history:", err);
      }
    });

    const exportQuizHistory = async () => {
      exporting.value = true;
      const token = localStorage.getItem("access_token");

      try {
        const res = await axios.post(
          "http://localhost:5000/user/export-quiz-history",
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const { task_id, message } = res.data;
        console.log("Export Task Started:", task_id);
        alert(
          "✅ Export started! You can check the CSV file shortly in the backend static folder."
        );
      } catch (error) {
        console.error("Export failed:", error);
        alert("❌ Export failed.");
      } finally {
        exporting.value = false;
      }
    };

    return {
      history,
      exporting,
      exportQuizHistory,
    };
  },
};
</script>

<style scoped>
.table th,
.table td {
  vertical-align: middle;
}
</style>
