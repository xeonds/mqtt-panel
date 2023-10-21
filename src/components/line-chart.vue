<template>
    <div id="main" :options="option" :data="data" />
</template>

<script lang="ts" setup>
import * as echarts from 'echarts';
import { defineProps } from "vue";
import {onMounted} from 'vue';
const props = defineProps({
    title: {
        type: String,
        default: "观测数据",
    },
    data: [Array, Object],
});
const randomData = ()=>{
  let now = new Date(+now + oneDay);
  let value = value + Math.random() * 21 - 10;
  return {
    name: now.toString(),
    value: [
      [now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'),
      Math.round(value)
    ]
  };
}

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

  // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option);
});
</script>

<style lang="less" scoped>
#main {
    height: 24rem;
    width: 100%;
}
</style>
