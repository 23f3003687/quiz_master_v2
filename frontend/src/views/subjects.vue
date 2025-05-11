<template>
  <div class="grid grid-cols-3 gap-4">
    <div
      v-for="subject in subjects"
      :key="subject.subject_id"
      class="bg-white p-4 rounded-lg shadow hover:shadow-lg transition duration-300"
    >
      <h3 class="text-lg font-semibold mb-2">{{ subject.name }}</h3>
      <p class="text-gray-600">{{ subject.description }}</p>
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
