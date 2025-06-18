<template>
  <div class="container mt-4">
    <h3>Search Quizzes & Subjects</h3>
    <div class="input-group mb-3">
      <select v-model="type" class="form-select w-auto">
        <option value="subjects">Subjects</option>
        <option value="quizzes">Quizzes</option>
      </select>
      <input
        type="text"
        v-model="query"
        class="form-control"
        placeholder="Search..."
      />
      <button class="btn btn-primary" @click="search">Search</button>
    </div>
    <div v-if="results.length">
      <div v-for="(item, i) in results" :key="i" class="card mb-2 p-2">
        <pre>{{ item }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      type: "subjects",
      query: "",
      results: [],
    };
  },
  methods: {
    async search() {
      try {
        const res = await axios.get(`/user/search/user`, {
          params: { type: this.type, query: this.query },
        });
        this.results = res.data;
      } catch (err) {
        alert("Search failed");
      }
    },
  },
};
</script>
