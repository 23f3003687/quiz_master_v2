<template>
  <div class="d-flex vh-100 overflow-hidden">
    <!-- Sidebar -->
    <Sidebar class="bg-dark text-white" />

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column" style="margin-left: 175px">
      <!-- Navbar -->
      <Navbar class="bg-white shadow-sm" />

      <div class="container mt-4">
        <h3 class="mb-4">📊 Admin Dashboard Summary</h3>

        <!-- Summary Cards -->
        <div class="row mb-4">
          <div class="col-md-3" v-for="card in summaryCards" :key="card.title">
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
            <PieChart :data="charts.pie" />
          </div>

          <div class="col-md-6 mb-4">
            <h5>Quizzes per Subject</h5>
            <BarChart :data="charts.bar" />
          </div>

          <div class="col-md-12 mb-4">
            <h5>Daily Attempts (Last 7 Days)</h5>
            <LineChart :data="charts.line" />
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
    const charts = ref({ pie: [], bar: [], line: [] });

    onMounted(async () => {
      const token = localStorage.getItem("access_token");
      try {
        const res = await axios.get("http://localhost:5000/admin/summary", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = res.data;
        summaryCards.value = [
          { title: "Total Users", value: data.total_users },
          { title: "Total Quizzes", value: data.total_quizzes },
          { title: "Total Subjects", value: data.total_subjects },
          { title: "Total Attempts", value: data.total_attempts },
        ];
        charts.value = {
          pie: data.pie_data,
          bar: data.bar_data,
          line: data.line_data,
        };
      } catch (err) {
        console.error("Failed to load summary:", err);
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
