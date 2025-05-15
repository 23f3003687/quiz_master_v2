<template>
  <div
    class="modal fade"
    id="editSubjectModal"
    tabindex="-1"
    aria-labelledby="editSubjectModalLabel"
    aria-hidden="true"
    ref="modalElement"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Subject</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">Subject Name</label>
            <input
              v-model="form.name"
              type="text"
              class="form-control"
              placeholder="Enter subject name"
            />
          </div>
          <div class="mb-3">
            <label class="form-label">Description</label>
            <textarea
              v-model="form.description"
              class="form-control"
              rows="3"
              placeholder="Enter description"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button type="button" class="btn btn-primary" @click="submitChanges">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from "bootstrap";
import axios from "axios";

export default {
  props: {
    subject: Object,
  },
  data() {
    return {
      modalInstance: null,
      form: {
        name: "",
        description: "",
      },
    };
  },
  methods: {
    open() {
      this.form.name = this.subject.name;
      this.form.description = this.subject.description;
      if (!this.modalInstance) {
        this.modalInstance = new Modal(this.$refs.modalElement);
      }
      this.modalInstance.show();
    },
    close() {
      if (this.modalInstance) {
        this.modalInstance.hide();
      }
    },
    async submitChanges() {
      try {
        const token = localStorage.getItem("access_token");

        const response = await axios.put(
          `http://localhost:5000/admin/subject/${this.subject.subject_id}`,
          {
            name: this.form.name,
            description: this.form.description,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        // Notify parent about update
        this.$emit("updated", response.data);

        // Close modal after successful update
        this.close();
        
        // Optional: show success alert or message here
        alert("Subject details updated successfully.");

      } catch (error) {
        console.error("Failed to update subject:", error);
        alert("Error updating subject");
      }
    },
  },
};
</script>
