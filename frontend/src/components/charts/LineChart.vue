<!-- src/components/charts/LineChart.vue -->
<template>
  <div class="chart-container">
    <Line :data="chartData" :options="options" />
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js';
import { Line } from 'vue-chartjs';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
);

export default {
  name: 'LineChart',
  components: { Line },
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
