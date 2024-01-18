<template>
  <div>
    <h1>监控面板</h1>
    <p>服务端连接状态: {{ isConn ? '已连接' : '未连接' }}</p>
    <el-button type="priamary" @click="exportData">导出数据</el-button>
    <el-divider />
    <div id="main" style="height: 24rem; width: 100%;" :option="drawChart"></div>
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
      _time: 1,
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
      this._time = 1
    },
    drawChart() {
      let option = {
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
        const [value] = event.data.split(',');
        this.borderPush(this.time, this._time++);
        this.borderPush(this.volts1, value);
        this.drawChart()
      });
    },
    borderPush(data, value) {
      if (data.length > 100) data.shift();
      data.push(value)
    },
    exportData() {
      const data = {
        time: this.time,
        volts1: this.volts1,
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
  }
}
</script>
