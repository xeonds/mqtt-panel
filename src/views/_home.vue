<template>
  <div>
    <h1>监控面板</h1>
    <el-row>
        <el-text>服务端连接状态: {{ isConn ? '已连接' : '未连接' }}</el-text>
        <el-button type="priamary" @click="exportData">导出数据</el-button>
    </el-row>
    <el-divider />
    <el-row>
        <el-col :span="12"> <div id="main1" style="height: 24rem; width: 100%;" :option="drawChart"></div> </el-col>
        <el-col :span="12"> <div id="main2" style="height: 24rem; width: 100%;" :option="drawChart"></div> </el-col>
    </el-row>
    <el-row>
        <el-col :span="12"> <div id="main3" style="height: 24rem; width: 100%;" :option="drawChart"></div> </el-col>
        <el-col :span="12"> <div id="main4" style="height: 24rem; width: 100%;" :option="drawChart"></div> </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
// socket接口部分，根据服务器地址协商修改
const socket = ref();
const addr = ref('ws://192.168.2.219/ws');
const isConn = ref(false);
// 四个统计图的控制对象
const chart1 = ref();
const chart2 = ref();
const chart3 = ref();
const chart4 = ref();
// 四个图表的数据源
const volts1 = ref([]);
const volts2 = ref([]);
const volts3 = ref([]);
const volts4 = ref([]);
// 时间记录
const time = ref([]);
const tick = ref(1);
// 初始化设定
onMounted(() => {
  socket.value = new WebSocket(addr.value);
  socket.value.addEventListener('open', () => { isConn.value = true; });
  socket.value.addEventListener('close', () => { isConn.value = false; });
  socket.value.addEventListener('message', (event: any) => {
    const [value] = event.data.split(',');
    borderPush(time.value, tick.value++);
    borderPush(volts1.value, value[0]);
    borderPush(volts2.value, value[1]);
    borderPush(volts3.value, value[2]);
    borderPush(volts4.value, value[3]);
    drawChart("传感器1", "电压1", volts1, chart1);
    drawChart("传感器2", "电压2", volts2, chart2);
    drawChart("传感器3", "电压3", volts3, chart3);
    drawChart("传感器4", "电压4", volts4, chart4);
  });
  initChart('main1', chart1)
  initChart('main2', chart2)
  initChart('main3', chart3)
  initChart('main4', chart4)
})
const initChart = (id: string, chart: any) => { chart.value = echarts.init(document.getElementById(id)); }
const drawChart = (title: string, tag: string, data: any, chart: any) => {
  let option = {
    title: { text: title },
    tooltip: {},
    legend: { data: [tag] },
    xAxis: { data: time.value, boundaryGap: false, },
    yAxis: {},
    series: [ { name: tag, type: "line", data: data.value }, ],
  }
  chart.value.setOption(option);
}
const borderPush = (data: any, value: any) => {
  if (data.length > 100) data.shift();
  data.push(value)
}
const exportData = () => {
  const data = {
    time: time.value,
    volts1: volts1.value,
    volts2: volts2.value,
    volts3: volts3.value,
    volts4: volts4.value
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
