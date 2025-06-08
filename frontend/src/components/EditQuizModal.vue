<template>
  <div
    class="modal fade show d-block"
    tabindex="-1"
    style="background: rgba(0, 0, 0, 0.5)"
  >
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header bg-dark text-white">
          <h5 class="modal-title">Edit Quiz</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="$emit('close')"
          ></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="submitUpdate">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Name</label>
                <input
                  v-model="form.name"
                  type="text"
                  class="form-control"
                  required
                />
              </div>


              <div class="col-md-6">
                <label class="form-label">Start Time</label>
                <input
                  v-model="form.start_datetime"
                  type="datetime-local"
                  class="form-control"
                />
              </div>

              <div class="col-md-6">
                <label class="form-label">Duration (minutes)</label>
                <input
                  v-model="form.time_duration"
                  type="text"
                  class="form-control"
                  required
                />
              </div>

              <div class="col-md-4">
                <label class="form-label">Total Marks</label>
                <input
                  v-model.number="form.total_marks"
                  type="number"
                  class="form-control"
                  required
                />
              </div>

              <div class="col-md-4">
                <label class="form-label">Questions</label>
                <input
                  v-model="form.num_questions"
                  type="text"
                  class="form-control"
                  required
                />
              </div>

              <div class="col-md-6">
                <label class="form-label">Remarks</label>
                <input
                  v-model="form.remarks"
                  type="text"
                  class="form-control"
                />
              </div>

              <div class="col-md-6">
                <label class="form-label">Tags (comma separated)</label>
                <input
                  v-model="form.tags"
                  type="text"
                  class="form-control"
                />
              </div>
            </div>

            <div class="mt-4 d-flex justify-content-end">
              <button type="submit" class="btn btn-success me-2">Update</button>
              <button
                type="button"
                class="btn btn-secondary"
                @click="$emit('close')"
              >
                Cancel
              </button>
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
      form: {
        ...this.quiz,
        start_datetime: this.quiz.start_datetime
          ? this.quiz.start_datetime.slice(0, 16) // ensure datetime-local format
          : "",
      },
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
        this.$emit("flash", {
          message: "Quiz updated successfully!",
          type: "success",
        });
        this.$emit("close");
      } catch (error) {
        this.$emit("flash", {
          message: "Failed to update quiz.",
          type: "danger",
        });
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
body {
  overflow: hidden;
}
</style>
