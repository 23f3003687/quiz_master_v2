<template>
  <div class="d-flex vh-100 overflow-hidden">
    <!-- Sidebar -->
    <UserSidebar class="bg-dark text-white" />

    <!-- Main content -->
    <div class="flex-grow-1 d-flex flex-column" style="margin-left: 175px">
      <!-- Navbar -->
      <UserNavbar class="bg-white shadow-sm" />

      <!-- Page Content -->
      <div class="container mt-4">
        <h4>Subjects</h4>
        <div class="row">
          <div
            class="col-md-3 mb-3"
            v-for="subject in subjects"
            :key="subject.subject_id"
          >
            <div
              class="card shadow-sm h-100 transition hover-card"
              @click="goToSubject(subject.subject_id)"
              style="cursor: pointer"
            >
              <div class="card-body">
                <h5 class="card-title">{{ subject.name }}</h5>
                <p class="card-text">{{ subject.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import UserSidebar from '@/components/UserSidebar.vue'
import UserNavbar from '@/components/UserNavbar.vue'

export default {
  name: 'UserSubjects',
  components: {
    UserSidebar,
    UserNavbar,
  },
  data() {
    return {
      subjects: [],
    }
  },
  mounted() {
    this.fetchSubjects()
  },
  methods: {
    fetchSubjects() {
      axios
        .get('http://localhost:5000/user/subjects', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        })
        .then((response) => {
          this.subjects = response.data.subjects
        })
        .catch((error) => {
          console.error('Error fetching subjects:', error)
        })
    },
    goToSubject(subjectId) {
       this.$router.push({ name: 'UserSubjectDetail', params: { subjectId } })
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

.hover-card:hover {
  background-color: rgb(200, 253, 255); /* light hover color */
  box-shadow: 0 4px 12px rgb(117, 25, 25); /* stronger shadow */
}
</style>
