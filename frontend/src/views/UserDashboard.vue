<template>
  <div class="container mt-4">
    <!-- User Greeting -->
    <div class="mb-4">
      <h4>Hello, {{ user.name }}</h4>
      <p>{{ currentDate }}</p>
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
            <h5 class="card-title">Last Active</h5>
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

    <!-- Student Activity -->
    <div>
      <h5>Recent Activity</h5>
      <ul class="list-group">
        <li
          class="list-group-item"
          v-for="activity in activityLog"
          :key="activity.id"
        >
          {{ activity.timestamp }} — {{ activity.description }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserDashboard',
  data() {
    return {
      user: {
        name: '',
        email: '',
        qualification: '',
      },
      currentDate: '',
      performance: 0,
      lastActive: '',
      quizzesCompleted: 0,
      activityLog: [],
    }
  },
  mounted() {
    this.currentDate = new Date().toLocaleDateString()
    this.fetchUserData()
  },
  methods: {
    fetchUserData() {
      axios
        .get('http://localhost:5000/user/dashboard', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        })
        .then((response) => {
          const data = response.data
          this.user = {
            name: data.full_name,
            email: data.email,
            qualification: data.qualification,
          }
          this.performance = data.performance
          this.lastActive = data.last_login
          this.quizzesCompleted = data.quizzes_completed
          this.activityLog = data.activity_log
        })
        .catch((error) => {
          console.error('Error fetching user dashboard:', error)
        })
    },
  },
}
</script>

<style scoped>
.card {
  transition: transform 0.2s;
}
.card:hover {
  transform: scale(1.02);
}
</style>
