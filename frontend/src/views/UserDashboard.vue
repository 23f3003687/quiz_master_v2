<template>
  <div class="d-flex vh-100 overflow-hidden">
    <!-- Sidebar on the left -->
    <UserSidebar class="bg-dark text-white" />

    <!-- Main content on the right -->
    <div
      class="flex-grow-1 d-flex flex-column"
      style="margin-left: 175px; max-height: 100vh; overflow-y: auto"
    >
      <!-- Navbar at the top -->
      <UserNavbar class="bg-white shadow-sm" />

      <!-- Main Dashboard Content -->
      <div class="container mt-4 pb-5">
        <!-- User Greeting -->
        <div class="mb-4">
          <h4>Hello, {{ user.full_name }}</h4>
          <p>{{ greetingMessage }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Qualification:</strong> {{ user.qualification }}</p>
        </div>

        <!-- Cards -->
        <div class="row mb-4">
          <div class="col-md-4">
            <div class="card text-white bg-primary shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Performance</h5>
                <p class="card-text">{{ performance }}%</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card text-white bg-info shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Last Login</h5>
                <p class="card-text">{{ lastActive }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card text-white bg-success shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Quizzes Completed</h5>
                <p class="card-text">{{ quizzesCompleted }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity Table -->
        <div>
          <h5>Recent Activity</h5>
          <div class="table-responsive">
            <table class="table table-striped table-bordered">
              <thead class="thead-dark">
                <tr>
                  <th>Quiz Name</th>
                  <th>Score</th>
                  <th>Accuracy (%)</th>
                  <th>Completion Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="activity in activityLog" :key="activity.id">
                  <td>{{ activity.quiz_name }}</td>
                  <td>{{ activity.score }}</td>
                  <td>{{ activity.accuracy }}</td>
                  <td>{{ activity.completion_date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UserSidebar from "@/components/UserSidebar.vue";
import UserNavbar from "@/components/UserNavbar.vue";

export default {
  name: "UserDashboard",
  components: {
    UserSidebar,
    UserNavbar,
  },
  data() {
    return {
      user: {
        full_name: "",
        email: "",
        qualification: "",
      },
      greetingMessage: "",
      performance: 0,
      lastActive: "",
      quizzesCompleted: 0,
      activityLog: [],
    };
  },
  mounted() {
    this.setGreeting();
    this.fetchUserData();
  },
  methods: {
    setGreeting() {
      const now = new Date();
      const hour = now.getHours();
      let greeting = "";

      if (hour < 12) greeting = "Good Morning";
      else if (hour < 17) greeting = "Good Afternoon";
      else greeting = "Good Evening";

      const dayName = now.toLocaleDateString("en-US", { weekday: "long" });
      const monthName = now.toLocaleDateString("en-US", { month: "long" });
      const date = now.getDate();
      const year = now.getFullYear();

      this.greetingMessage = `${greeting} | ${dayName}, ${monthName} ${date}, ${year}`;
    },
    fetchUserData() {
      axios
        .get("http://localhost:5000/user/dashboard", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          const data = response.data;
          this.user = {
            full_name: data.full_name,
            email: data.email,
            qualification: data.qualification,
          };
          this.performance = data.performance;
          this.lastActive = data.last_login;
          this.quizzesCompleted = data.quizzes_completed;
          this.activityLog = data.activity_log;
        })
        .catch((error) => {
          console.error("Error fetching user dashboard:", error);
        });
    },
  },
};
</script>

<style scoped>
.card {
  transition: transform 0.2s;
}
.card:hover {
  transform: scale(1.02);
}
</style>
