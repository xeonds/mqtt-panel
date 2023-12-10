<template>
  <div>
    <h1>Vue WebSocket Example</h1>
    <div id="main" style="height: 24rem; width: 100%;" :option="drawChart"></div>
    <p>服务端连接状态: {{ isConn ? '已连接' : '未连接' }}</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
export default {
  data() {
    return {
      chart: null,
      socket: null,
      addr: 'ws://192.168.2.219/ws',
      time: [],
      volts1: [],
      isConn: false,
    }
  },
  mounted() {
    this.initChart()
    this.drawChart()
    this.initWebSocket();
  },
  methods: {
    initChart() {
      this.chart = echarts.init(document.getElementById('main'));
    },
    drawChart() {
      let option= {
        title: { text: '传感器观测数据' },
        tooltip: {},
        legend: {
          data: ["电压1"]
        },
        xAxis: {
          data: this.time,
          boundaryGap: false,
        },
        yAxis: {},
        series: [
          {
            name: "电压1",
            type: "line",
            data: this.volts1
          },
        ],
      }
      this.chart.setOption(option);
    },
    initWebSocket() {
      this.socket = new WebSocket(this.addr);
      this.socket.addEventListener('open', () => {
        this.isConn = true;
        console.log('connected')
      });
      this.socket.addEventListener('close', () => {
        this.isConn = false;
        console.log('disconnected')
      });
      this.socket.addEventListener('message', (event) => {
        const [value, timestamp] = event.data.split(',');
        this.time.push(timestamp)
        this.volts1.push(value)
        this.drawChart()
      });
    }
  }
}
</script>
