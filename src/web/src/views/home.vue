<template>
  <div>
    <h1>监控面板</h1>
    <el-divider />
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

<script>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
export default {
  data() {
    return {
      chart1: null,
      chart2: null,
      chart3: null,
      chart4: null,
      socket: null,
      addr: 'ws://123.56.246.71:8765/ws',
      time: [],
      _time: 1,
      volts1: [],
      volts2: [],
      volts3: [],
      volts4: [],
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
      this.chart1 = echarts.init(document.getElementById('main1'));
      this.chart2 = echarts.init(document.getElementById('main2'));
      this.chart3 = echarts.init(document.getElementById('main3'));
      this.chart4 = echarts.init(document.getElementById('main4'));
      this._time = 1
    },
    drawChart() {
      let option1 = {
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
      this.chart1.setOption(option1);

      let option2 = {
        title: { text: '传感器观测数据' },
        tooltip: {},
        legend: {
          data: ["电压2"]
        },
        xAxis: {
          data: this.time,
          boundaryGap: false,
        },
        yAxis: {},
        series: [
          {
            name: "电压2",
            type: "line",
            data: this.volts2
          },
        ],
      }
      this.chart2.setOption(option2);

      let option3 = {
        title: { text: '传感器观测数据' },
        tooltip: {},
        legend: {
          data: ["电压3"]
        },
        xAxis: {
          data: this.time,
          boundaryGap: false,
        },
        yAxis: {},
        series: [
          {
            name: "电压3",
            type: "line",
            data: this.volts3
          },
        ],
      }
      this.chart3.setOption(option3);

      let option4 = {
        title: { text: '传感器观测数据' },
        tooltip: {},
        legend: {
          data: ["电压4"]
        },
        xAxis: {
          data: this.time,
          boundaryGap: false,
        },
        yAxis: {},
        series: [
          {
            name: "电压4",
            type: "line",
            data: this.volts4
          },
        ],
      }
      this.chart4.setOption(option4);
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
        const value = event.data.split(',');
        this.borderPush(this.time, this._time++);
        this.borderPush(this.volts1, value[0]);
        this.borderPush(this.volts2, value[1]);
        this.borderPush(this.volts3, value[2]);
        this.borderPush(this.volts4, value[3]);
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
        volts2: this.volts2,
        volts3: this.volts3,
        volts4: this.volts4,
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
