<template>
  <div class="d-flex min-vh-100">
    <!-- Sidebar -->
    <UserSidebar class="bg-dark text-white" />

    <!-- Main content -->
    <div class="flex-grow-1 d-flex flex-column" style="margin-left: 175px">
      <!-- Navbar -->
      <UserNavbar class="bg-white shadow-sm" />

      <!-- Page content -->
      <div class="container" style="padding-top: 80px; padding-bottom: 40px">
        <h3 class="mb-4">📊 Quiz Summary Report</h3>

        <!-- Summary Cards -->
        <div class="row mb-4">
          <div
            class="col-md-4"
            v-for="(card, index) in summaryCards"
            :key="index"
          >
            <div class="card shadow-sm text-center">
              <div class="card-body">
                <h5 class="card-title">{{ card.label }}</h5>
                <h3 class="card-text">{{ card.value }}</h3>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts -->
        <div class="row mb-4">
          <div class="col-md-6">
            <h5 class="text-center">Pass vs Fail Distribution (Pie Chart)</h5>
            <PieChart
              v-if="pieData && pieData.labels"
              :chart-data="pieData"
              :options="pieOptions"
            />
          </div>

          <div class="col-md-6">
            <h5 class="text-center">Score Trend Over Time (Line Chart)</h5>
            <LineChart
              v-if="lineData && lineData.labels"
              :chart-data="lineData"
              :options="lineOptions"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import UserSidebar from "@/components/UserSidebar.vue";
import UserNavbar from "@/components/UserNavbar.vue";
import PieChart from "@/components/charts/PieChart.vue";
import LineChart from "@/components/charts/LineChart.vue";

export default {
  name: "QuizSummary",
  components: {
    UserSidebar,
    UserNavbar,
    PieChart,
    LineChart,
  },
  setup() {
    const summaryCards = ref([]);
    const pieData = ref({});
    const pieOptions = ref({});
    const lineData = ref({});
    const lineOptions = ref({});

    onMounted(async () => {
      const token = localStorage.getItem("access_token");
      try {
        const res = await axios.get(
          "http://localhost:5000/user/summary-report",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        const summary = res.data.summary || {};
        const scores = res.data.scores || [];

        // Summary cards from summary object
        summaryCards.value = [
          { label: "Quizzes Attempted", value: summary.total_quizzes || 0 },
          {
            label: "Average Score",
            value: summary.average_score ? summary.average_score + "%" : "N/A",
          },
          {
            label: "Pass Rate",
            value: summary.total_quizzes
              ? ((summary.passed / summary.total_quizzes) * 100).toFixed(1) +
                "%"
              : "N/A",
          },
        ];

        // Pie Chart - Pass vs Fail Distribution
        const passCount = scores.filter((s) => s.status === "PASSED").length;
        const failCount = scores.length - passCount;

        pieData.value = {
          labels: ["Passed", "Failed"],
          datasets: [
            {
              data: [passCount, failCount],
              backgroundColor: ["#28a745", "#dc3545"],
            },
          ],
        };

        pieOptions.value = {
          responsive: true,
          plugins: { legend: { position: "bottom" } },
        };

        // Line Chart - Score trend over time
        lineData.value = {
          labels: scores.map((s) =>
            new Date(s.time_stamp_of_attempt).toLocaleDateString()
          ),
          datasets: [
            {
              label: "Score",
              data: scores.map((s) => s.total_score),
              borderColor: "#6610f2",
              tension: 0.3,
              fill: false,
            },
          ],
        };

        lineOptions.value = {
          responsive: true,
          plugins: { legend: { position: "top" } },
        };
      } catch (err) {
        console.error("Failed to load summary report:", err);
      }
    });

    return {
      summaryCards,
      pieData,
      pieOptions,
      lineData,
      lineOptions,
    };
  },
};
</script>

<style scoped>
.container-fluid {
  max-height: calc(100vh - 56px);
}
</style>
