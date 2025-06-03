<template>
  <div class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header bg-dark text-white">
          <h5 class="modal-title">Edit Quiz</h5>
          <button type="button" class="btn-close btn-close-white" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="submitUpdate">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Name</label>
                <input v-model="form.name" type="text" class="form-control" required />
              </div>

              <div class="col-md-6">
                <label class="form-label">Date of Quiz</label>
                <input v-model="form.date_of_quiz" type="date" class="form-control" required />
              </div>

              <div class="col-md-4">
                <label class="form-label">Duration (minutes)</label>
                <input v-model="form.time_duration" type="text" class="form-control" required />
              </div>

              <div class="col-md-4">
                <label class="form-label">Total Marks</label>
                <input v-model.number="form.total_marks" type="number" class="form-control" required />
              </div>

              <div class="col-md-4">
                <label class="form-label">Questions</label>
                <input v-model="form.num_questions" type="text" class="form-control" required />
              </div>

              <div class="col-md-6">
                <label class="form-label">Remarks</label>
                <input v-model="form.remarks" type="text" class="form-control" />
              </div>

              <div class="col-md-6">
                <label class="form-label">Tags (comma separated)</label>
                <input v-model="form.tags" type="text" class="form-control" />
              </div>
            </div>

            <div class="mt-4 d-flex justify-content-end">
              <button type="submit" class="btn btn-success me-2">Update</button>
              <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
            </div>
          </form>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    quiz: Object,
  },
  data() {
    return {
      form: { ...this.quiz },
    };
  },
  methods: {
    async submitUpdate() {
      try {
        const token = localStorage.getItem("access_token");
        await axios.put(
          `http://localhost:5000/admin/quizzes/${this.form.quiz_id}`,
          JSON.stringify(this.form),
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
        this.$emit("updated");
        this.$emit("close");
      } catch (error) {
        alert("Failed to update quiz.");
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
/* Optional: prevent background scroll when modal is open */
body {
  overflow: hidden;
}
</style>
