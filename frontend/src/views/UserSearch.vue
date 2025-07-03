<template>
  <div class="d-flex vh-100 overflow-hidden">
    <!-- Sidebar -->
    <Sidebar class="bg-dark text-white" />

    <!-- Main content -->
    <div class="flex-grow-1 d-flex flex-column">
      <!-- Navbar -->
      <UserNavbar class="bg-white shadow-sm" />

      <!-- Content container -->
      <div class="container mt-4 pt-5 flex-grow-1 overflow-auto">
        <h3 class="mb-4">Search Results</h3>

        <div v-if="loading" class="text-muted">Loading...</div>
        <div v-else-if="results.length === 0" class="text-danger">
          No results found.
        </div>

        <div v-else>
          <div
            v-for="(item, index) in results"
            :key="index"
            class="card mb-3 shadow-sm"
            style="cursor: pointer"
            @click="goToDetailPage(item)"
          >
            <div class="card-body">
              <h5 class="card-title text-primary">
                {{ getTitle(item) }}
                <span class="badge bg-secondary text-capitalize float-end">
                  {{ item.type }}
                </span>
              </h5>
              <hr />
              <div
                v-for="(value, key) in item"
                :key="key"
                v-if="key !== 'type' && !isTitleKey(key)"
                class="mb-1"
              >
                <strong class="text-capitalize">{{ formatKey(key) }}:</strong>
                <span>{{ value }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Sidebar from "@/components/UserSidebar.vue";
import UserNavbar from "@/components/UserNavbar.vue";

export default {
  name: "UserSearch",
  components: {
    Sidebar,
    UserNavbar,
  },
  data() {
    return {
      results: [],
      loading: false,
    };
  },
  methods: {
    async fetchResults() {
      const query = this.$route.query.query;
      if (!query) return;

      this.loading = true;

      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          `http://localhost:5000/user/search?query=${encodeURIComponent(
            query
          )}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (Array.isArray(response.data)) {
          this.results = response.data;
        } else {
          this.results = [];
        }
      } catch (error) {
        console.error("User search failed:", error);
        this.results = [];
      } finally {
        this.loading = false;
      }
    },

    getTitle(item) {
      return item.name || "Result";
    },
    isTitleKey(key) {
      return ["name"].includes(key);
    },
    formatKey(key) {
      return key.replace(/_/g, " ");
    },

    goToDetailPage(item) {
      if (item.type === "subject") {
        this.$router.push(`/user/subject/${item.subject_id}`);
      } else if (item.type === "quiz") {
        this.$router.push({
          name: "QuizAttempt",
          params: { quizId: item.quiz_id },
          query: { subjectId: item.subject_id || null },
        });
      } else {
        console.warn("Navigation not defined for this type.");
      }
    },
  },
  mounted() {
    this.fetchResults();
  },
  watch: {
    "$route.query.query": "fetchResults",
  },
};
</script>

<style scoped>
.card-title {
  margin-bottom: 0.5rem;
  font-weight: 600;
}
</style>
