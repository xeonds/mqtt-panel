<template>
  <div id="main" :options="option" :data="data"></div>
</template>

<script lang="ts" setup>
import * as echarts from 'echarts';
import { onMounted } from 'vue';

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
  var chartDom = document.getElementById("main")!;
  var myChart = echarts.init(chartDom);
  var option = {
    title: {
      text: props.title,
    },
    tooltip: {
      trigger: "axis",
    },
    legend: {
      data: ["压力"],
    },
    xAxis: {
      type: "time",
      splitLine: {
        show: false
      }
    },
    yAxis: {
      type: "value",
      boundaryGap: [0, '100%'],
      splitLine: {
        show: false
      }
    },
    series: [
      {
        name: "压力传感器1",
        type: "line",
        showSymbol: false,
        data: props.data || [5, 20, 36, 10, 10, 20]
      },
    ],
  };
  myChart.setOption(option);
});
</script>

<style lang="less" scoped>
#main {
  height: 100%;
  width: 100%;
}
</style>
