<template>
  <div class="row">
    <div
      v-for="subject in subjects"
      :key="subject.subject_id"
      class="col-md-3 mb-3"
    >
      <router-link
        :to="'/admin/subject/' + subject.subject_id"
        class="text-decoration-none text-dark"
      >
        <div class="card shadow-sm h-100 transition hover-card">
          <div class="card-body">
            <h5 class="card-title fs-4">{{ subject.name }}</h5>
            <!-- Larger title -->
            <p class="card-text text-muted fs-6">{{ subject.description }}</p>
            <!-- Smaller description -->
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "Subjects",
  props: {
    subjects: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>

.card {
  transition: transform 0.2s;
}
.card:hover {
  transform: scale(1.02);
}
.hover-card:hover {
  background-color:rgb(173, 225, 255); /* light grey hover effect */
  box-shadow: 0 4px 12px rgb(117, 25, 25); /* stronger shadow on hover */
}
</style>
