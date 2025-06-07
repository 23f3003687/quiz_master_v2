<!-- src/components/charts/PieChart.vue -->
<template>
  <div class="chart-container">
    <Pie :data="chartData" :options="options" />
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { Pie } from 'vue-chartjs';

ChartJS.register(Title, Tooltip, Legend, ArcElement);

export default {
  name: 'PieChart',
  components: { Pie },
  props: {
    chartData: { type: Object, required: true },
    options: { type: Object, default: () => ({ responsive: true, maintainAspectRatio: false }) }
  }
};
</script>

<style scoped>
.chart-container {
  height: 300px;
}
</style>
