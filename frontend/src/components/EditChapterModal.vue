<template>
  <div
    class="modal fade"
    tabindex="-1"
    role="dialog"
    ref="modal"
    aria-labelledby="editChapterModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <form @submit.prevent="submitEdit">
          <div class="modal-header">
            <h5 class="modal-title" id="editChapterModalLabel">Edit Chapter</h5>
            <button
              type="button"
              class="btn-close"
              aria-label="Close"
              @click="hide"
            ></button>
          </div>

          <div class="modal-body">
            <div v-if="errorMessage" class="alert alert-danger">
              {{ errorMessage }}
            </div>

            <div class="mb-3">
              <label for="chapterName" class="form-label">Chapter Name</label>
              <input
                id="chapterName"
                v-model="editedChapter.name"
                type="text"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3">
              <label for="chapterDescription" class="form-label"
                >Description</label
              >
              <textarea
                id="chapterDescription"
                v-model="editedChapter.description"
                class="form-control"
                rows="3"
              ></textarea>
            </div>

            <div class="mb-3">
              <label for="difficultyLevel" class="form-label"
                >Difficulty Level</label
              >
              <select
                id="difficultyLevel"
                v-model="editedChapter.difficulty_level"
                class="form-select"
                required
              >
                <option disabled value="">Select difficulty</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="hide">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span
                v-if="loading"
                class="spinner-border spinner-border-sm me-2"
              ></span>
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditChapterModal",
  props: {
    chapter: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      editedChapter: {
        chapter_id: null,
        name: "",
        description: "",
        difficulty_level: "",
      },
      modalInstance: null,
      loading: false,
      errorMessage: "",
    };
  },
  watch: {
    chapter: {
      immediate: true,
      handler(newChapter) {
        this.editedChapter = { ...newChapter };
      },
    },
  },
  methods: {
    open() {
      // Reset form data
      this.editedChapter = { ...this.chapter };
      this.errorMessage = "";
      this.loading = false;

      if (!this.modalInstance) {
        this.modalInstance = new bootstrap.Modal(this.$refs.modal);
      }
      this.modalInstance.show();
    },
    hide() {
      if (this.modalInstance) {
        this.modalInstance.hide();
      }
    },
    async submitEdit() {
      this.loading = true;
      this.errorMessage = "";
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.put(
          `http://localhost:5000/admin/chapters/${this.editedChapter.chapter_id}`,
          {
            name: this.editedChapter.name,
            description: this.editedChapter.description,
            difficulty_level: this.editedChapter.difficulty_level,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.$emit("updated", response.data);
        this.hide();
      } catch (error) {
        console.error("Failed to update chapter:", error);
        this.errorMessage =
          error.response?.data?.message || "Failed to update chapter";
        this.$emit("error", this.errorMessage);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Optional scoped custom styling */
</style>
