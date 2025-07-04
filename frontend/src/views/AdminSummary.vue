<template>
  <div class="d-flex min-vh-100">
    <!-- Sidebar -->
    <Sidebar class="bg-dark text-white" />

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column" >
      <!-- Navbar -->
      <Navbar class="bg-white shadow-sm" />

      <div class="container mt-5 pt-5">
        <h3 class="mb-4 ">📊 Summary</h3>

        <!-- Summary Cards -->
        <div class="row mb-4">
          <div class="col-md-4" v-for="card in summaryCards" :key="card.title">
            <div class="card text-center shadow-sm">
              <div class="card-body">
                <h5 class="card-title">{{ card.title }}</h5>
                <p class="display-6 fw-bold">{{ card.value }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts -->
        <div class="row">
          <div class="col-md-6 mb-4">
            <h5>Quiz Attempts by Subject</h5>
            <PieChart v-if="charts.pie" :chart-data="charts.pie" />
          </div>

          <div class="col-md-6 mb-4">
            <h5>Quizzes per Subject</h5>
            <BarChart v-if="charts.bar" :chart-data="charts.bar" />
          </div>

          <div class="col-md-12 mb-4">
            <h5>Daily Attempts (Last 7 Days)</h5>
            <LineChart v-if="charts.line" :chart-data="charts.line" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import Sidebar from "@/components/sidebar.vue";
import Navbar from "@/components/navbar.vue";
import PieChart from "@/components/charts/PieChart.vue";
import BarChart from "@/components/charts/BarChart.vue";
import LineChart from "@/components/charts/LineChart.vue";

export default {
  name: "AdminSummary",
  components: {
    Sidebar,
    Navbar,
    PieChart,
    BarChart,
    LineChart,
  },
  setup() {
    const summaryCards = ref([]);
    const charts = ref({
      pie: null,
      bar: null,
      line: null,
    });

    onMounted(async () => {
      const token = localStorage.getItem("access_token");

      try {
        const res = await axios.get(
          "http://localhost:5000/admin/summary-report",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const summary = res.data.summary;
        const scores = res.data.scores || [];

        // 🟩 Summary cards
        summaryCards.value = [
          { title: "Total Users", value: summary.total_users },
          { title: "Total Quizzes", value: summary.total_quizzes },
          { title: "Total Subjects", value: summary.total_subjects },
        ];

        // 🟧 Pie Chart (Quiz Attempts by Subject)
        const subjectAttempts = scores.filter(
          (s) => s.type === "subject_attempts"
        );
        charts.value.pie = {
          labels: subjectAttempts.map((s) => s.label),
          datasets: [
            {
              data: subjectAttempts.map((s) => s.value),
              backgroundColor: [
                "#007bff",
                "#28a745",
                "#ffc107",
                "#dc3545",
                "#6f42c1",
              ],
            },
          ],
        };

        // 🟦 Bar Chart (Quizzes per Subject)
        const subjectQuizzes = scores.filter(
          (s) => s.type === "subject_quizzes"
        );
        charts.value.bar = {
          labels: subjectQuizzes.map((s) => s.label),
          datasets: [
            {
              label: "Quizzes",
              data: subjectQuizzes.map((s) => s.value),
              backgroundColor: "#17a2b8",
            },
          ],
        };

        // 🟪 Line Chart (Daily Attempts)
        const dailyAttempts = scores.filter((s) => s.type === "daily_attempts");
        charts.value.line = {
          labels: dailyAttempts.map((s) => s.label),
          datasets: [
            {
              label: "Attempts",
              data: dailyAttempts.map((s) => s.value),
              borderColor: "#6610f2",
              tension: 0.4,
              fill: false,
            },
          ],
        };
      } catch (err) {
        console.error("❌ Failed to load summary data:", err);
      }
    });

    return {
      summaryCards,
      charts,
    };
  },
};
</script>

<style scoped>
.card-title {
  font-size: 1.1rem;
  color: #555;
}
</style>
