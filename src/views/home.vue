<template>
  <div>
    <h1>Vue WebSocket Example</h1>
    <lineChart :data="data" />
    <p>Status: {{ status }}</p>
    <p>Data: {{ data }}</p>
  </div>
</template>

<script setup lang="ts">
import lineChart from '../components/line-chart.vue'
import { ref, onMounted } from 'vue';

const data = ref([]); // 用于存储ECharts数据
const status = ref([]); // 用于存储ECharts数据

const initializeWebSocket = () => {
  const socket = new WebSocket('/ws');
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    data.value = data;
  };
};

onMounted(() => {
  initializeWebSocket();
});
</script>
