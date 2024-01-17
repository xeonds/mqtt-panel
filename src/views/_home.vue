<template>
  <div>
    <h1>Vue WebSocket Example</h1>
    <div id="main" style="height: 24rem; width: 100%;" :option="drawChart"></div>
    <p>服务端连接状态: {{ isConn ? '已连接' : '未连接' }}</p>
    <el-button type="priamary" @click="exportData">导出数据</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
const chart = ref();
const socket = ref();
const addr = ref('ws://192.168.2.219/ws');
const time = ref([]);
const _time = ref(1);
const volts1 = ref([]);
const isConn = ref(false);
onMounted(() => {
  initChart()
  drawChart()
  initWebSocket();
})
const initChart = () => {
  chart.value = echarts.init(document.getElementById('main'));
  _time.value = 1
}
const drawChart =() => {
  let option = {
    title: { text: '传感器观测数据' },
    tooltip: {},
    legend: {
      data: ["电压1"]
    },
    xAxis: {
      data: time.value,
      boundaryGap: false,
    },
    yAxis: {},
    series: [
      {
        name: "电压1",
        type: "line",
        data: volts1.value
      },
    ],
  }
  chart.value.setOption(option);
}
const initWebSocket = () => {
  socket.value = new WebSocket(addr.value);
  socket.value.addEventListener('open', () => {
    isConn.value = true;
    console.log('connected')
  });
  socket.value.addEventListener('close', () => {
    isConn.value = false;
    console.log('disconnected')
  });
  socket.value.addEventListener('message', (event: any) => {
    const [value] = event.data.split(',');
    borderPush(time.value, _time.value++);
    borderPush(volts1.value, value);
    drawChart()
  });
}
const borderPush = (data:any, value:any) => {
  if (data.length > 100) data.shift();
  data.push(value)
}
const exportData = () => {
  const data = {
    time: time.value,
    volts1: volts1.value,
  }
  const blob = new Blob([JSON.stringify(data)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = "data.json";
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
</script>
