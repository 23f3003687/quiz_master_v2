<template>
  <div
    class="modal fade show d-block"
    tabindex="-1"
    style="background-color: rgba(0, 0, 0, 0.5)"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
          <h5 class="modal-title">Edit Question</h5>
          <button
            type="button"
            class="btn-close"
            @click="$emit('close')"
          ></button>
        </div>


        <!-- Modal Body -->
        <div class="modal-body">
          <form @submit.prevent="updateQuestion">
            <div class="mb-3">
              <label class="form-label">Question Statement</label>
              <textarea
                v-model="form.question_statement"
                class="form-control"
                required
              />
            </div>

            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Option 1</label>
                <input v-model="form.option1" class="form-control" required />
              </div>
              <div class="col-md-6">
                <label class="form-label">Option 2</label>
                <input v-model="form.option2" class="form-control" required />
              </div>
              <div class="col-md-6">
                <label class="form-label">Option 3</label>
                <input v-model="form.option3" class="form-control" required />
              </div>
              <div class="col-md-6">
                <label class="form-label">Option 4</label>
                <input v-model="form.option4" class="form-control" required />
              </div>
              <div class="col-md-6">
                <label class="form-label">Correct Option</label>
                <select
                  v-model="form.correct_option"
                  class="form-select"
                  required
                >
                  <option value="option1">Option 1</option>
                  <option value="option2">Option 2</option>
                  <option value="option3">Option 3</option>
                  <option value="option4">Option 4</option>
                </select>
              </div>
              <div class="col-md-6">
                <label class="form-label">Difficulty</label>
                <input
                  v-model="form.difficulty"
                  class="form-control"
                  placeholder="Easy, Medium, Hard"
                />
              </div>
              <div class="col-md-12">
                <label class="form-label">Explanation</label>
                <textarea
                  v-model="form.explanation"
                  class="form-control"
                  rows="3"
                />
              </div>
            </div>
          </form>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            @click="$emit('close')"
          >
            Cancel
          </button>
          <button type="button" class="btn btn-primary" @click="updateQuestion">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditQuestionModal",
  props: {
    question: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        question_id: null,
        quiz_id: null,
        question_statement: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_option: "",
        difficulty: "",
        explanation: "",
      },
      showFlash: false,
      flashMessage: "",
      flashType: "", // success, danger, etc.
    };
  },
  methods: {
    async updateQuestion() {
      try {
        const token = localStorage.getItem("access_token");
        await axios.put(
          `http://localhost:5000/admin/questions/${this.form.question_id}`,
          JSON.stringify(this.form),
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        // Emit flash event to parent
        this.$emit("flash", {
          message: "Question updated successfully!",
          type: "success",
        });

        // Emit updated and close events
        this.$emit("updated");
        this.$emit("close");
      } catch (error) {
        // Emit error flash to parent
        this.$emit("flash", {
          message:
            error.response?.data?.message || "Failed to update question.",
          type: "danger",
        });

        console.error("Failed to update question:", error);
      }
    },
  },
  mounted() {
    this.form = { ...this.question };
  },
};
</script>

<style scoped>
.modal {
  z-index: 1050;
}
</style>
