<template>
  <div>
    <h1>Vue WebSocket Example</h1>
    <lineChart style="height: 24rem; width: 100%;" :title="'传感器观测数据'" :data="data" />
    <p>Status: {{ isConn?'已连接':'未连接' }}</p>
  </div>
</template>

<script setup lang="ts">
import lineChart from '../components/line-chart.vue'
import { ref, onMounted } from 'vue';

const data = ref([]); // 用于存储ECharts数据
const isConn = ref(false);
const socket = new WebSocket('/ws');

const initializeWebSocket = () => {
  socket.addEventListener('open', () => {
    isConn.value = true;
  });

  socket.addEventListener('close', () => {
    isConn.value = false;
  });

  socket.addEventListener('message', (event) => {
    const message = event.data;
    console.log('Received message:', message);
  });
};

onMounted(() => {
  initializeWebSocket();
});
</script>
