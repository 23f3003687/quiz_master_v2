<template>
  <div class="d-flex min-vh-100">
    <!-- Sidebar -->
    <UserSidebar class="bg-dark text-white" />

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column" style="margin-left: 175px">
      <!-- Navbar -->
      <UserNavbar class="bg-white shadow-sm" />

      <div class="container" style="padding-top: 80px; padding-bottom: 40px">
        <!-- Heading + Export Button on the same line -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="mb-0">📘 Quiz History</h3>
          <button
            class="btn btn-outline-success"
            @click="exportQuizHistory"
            :disabled="exporting"
          >
            <span v-if="exporting">📤 Exporting...</span>
            <span v-else>📥 Export Quiz History</span>
          </button>
        </div>

        <!-- Download link or error alert -->
        <div v-if="downloadUrl" class="alert alert-success">
          ✅ Export ready.
          <a :href="downloadUrl" download target="_blank"
            >Click to Download CSV</a
          >
        </div>

        <div v-if="exportError" class="alert alert-danger">
          ❌ {{ exportError }}
        </div>

        <!-- Quiz History Table -->
        <div v-if="history.length === 0" class="alert alert-info">
          No quiz attempts found.
        </div>

        <table v-else class="table table-striped shadow-sm">
          <thead class="custom-thead">
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
    const downloadUrl = ref("");
    const exportError = ref("");

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

        const { task_id } = res.data;
        checkStatus(task_id); // start polling
      } catch (err) {
        console.error("Export failed:", err);
        alert("❌ Export failed.");
        exporting.value = false;
      }
    };

    const checkStatus = async (taskId) => {
      const token = localStorage.getItem("access_token");

      const interval = setInterval(async () => {
        try {
          const res = await axios.get(
            `http://localhost:5000/user/export-status/${taskId}`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );

          if (res.data.status === "ready") {
            clearInterval(interval);
            alert("✅ Export complete! Downloading now...");
            // ✅ Trigger browser download
            const link = document.createElement("a");
            link.href = res.data.download_url;
            link.download = ""; // Let browser use filename from server
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            exporting.value = false;
          }
        } catch (err) {
          console.error("Error checking export status:", err);
          clearInterval(interval);
          exporting.value = false;
          alert("❌ Error while checking task status.");
        }
      }, 3000); // poll every 3 seconds
    };

    return {
      history,
      exporting,
      downloadUrl,
      exportError,
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

.custom-thead,
.custom-thead th {
  background-color: #032d45 !important;
  color: white !important;
}
</style>
