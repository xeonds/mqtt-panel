<template>
  <div>
    <h2>{{ props.title }}</h2>
    <div id="main" style="height: 24rem; width: 100%;" :option="drawChart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
// data
const chart = ref();
const time = ref([]);
const _time = ref(1);
const volts1 = ref([]);
// props
const props = defineProps({
  title: {
    type: String,
    default: "观测数据",
  },
  data: [Array, Object],
  option: {
    type: Object,
    default: () => { return { xAxis: { type: "time", } } }
  }
});
onMounted(() => {
  initChart()
  drawChart()
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
const borderPush = (data:any, value:any) => {
  if (data.length > 100) data.shift();
  data.push(value)
}
const exportData = (time: any, volts: any) => {
  const data = {
    time: time.value,
    ...volts.value
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
<style lang="less" scoped>
#main {
  height: 100%;
  width: 100%;
}
</style>

