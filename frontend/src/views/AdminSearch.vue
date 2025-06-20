<template>
  <div class="d-flex vh-100 overflow-hidden">
    <!-- Sidebar on the left -->
    <Sidebar class="bg-dark text-white" />

    <!-- Main content on the right -->
    <div class="flex-grow-1 d-flex flex-column">
      <!-- Navbar at the top -->
      <Navbar class="bg-white shadow-sm" />

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
import Sidebar from "@/components/sidebar.vue";
import Navbar from "@/components/navbar.vue";

export default {
  name: "AdminSearch",
  components: { Sidebar, Navbar },
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
          `http://localhost:5000/admin/search/admin?query=${encodeURIComponent(
            query
          )}`,

          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        // ✅ Defensive check to make sure response is an array
        if (Array.isArray(response.data)) {
          this.results = response.data.map((item) => {
            if (item.email) return { ...item, type: "user" };
            if (item.description) return { ...item, type: "subject" };
            if (item.chapter_id && item.subject_name)
              return { ...item, type: "quiz" };
            if (item.question) return { ...item, type: "question" };
            return { ...item, type: "unknown" };
          });
        } else {
          // Not an array: maybe it's an error object
          console.error("Unexpected response format:", response.data);
          this.results = [];
        }
      } catch (error) {
        console.error("Search failed:", error);
        this.results = [];
      } finally {
        this.loading = false;
      }
    },

    getTitle(item) {
      return item.name || item.question || item.email || "Result";
    },
    isTitleKey(key) {
      return ["name", "question", "email"].includes(key);
    },
    formatKey(key) {
      return key.replace(/_/g, " ");
    },
    goToDetailPage(item) {
      if (item.type === "user") {
        this.$router.push(`/users`);
      } else if (item.type === "subject") {
        const subjectId = item.subject_id || item.id; // 🔑 Corrected ID
        this.$router.push(`/admin/subject/${subjectId}`);
      } else if (item.type === "chapter") {
        this.$router.push(`/admin/subject/${item.subject_id}`);
      } else if (item.type === "quiz") {
        const chapterId = item.chapter_id;
        const chapterName = item.chapter_name || item.subject_name || "chapter";
        this.$router.push({
          name: "QuizList",
          params: { chapterId, chapterName },
        });
      } else if (item.type === "question") {
        alert("Navigation for individual question not implemented.");
      } else {
        console.warn("Unknown type. Cannot navigate.");
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
