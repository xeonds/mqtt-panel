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

const data = ref(<any>[]);
const isConn = ref(false);
const socket = new WebSocket('ws://localhost:8080/ws');

const initializeWebSocket = () => {
  socket.addEventListener('open', () => {
    isConn.value = true;
    console.log('connected')
  });

  socket.addEventListener('close', () => {
    isConn.value = false;
    console.log('disconnected')
  });

  socket.addEventListener('message', (event) => {
    const message = event.data;
    console.log(message)
    data.value.push(JSON.parse(message));
  });
};

onMounted(() => {
  initializeWebSocket();
});
</script>
