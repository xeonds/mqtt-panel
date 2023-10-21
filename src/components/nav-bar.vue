<template>
  <el-menu
    :default-active="activeIndex"
    mode="horizontal"
    :ellipsis="false"
    id="nav"
  >
    <el-menu-item @click="go('/')" index="0">
        MQTT Panel
    </el-menu-item>
    <div class="flex-grow"></div>
    <el-menu-item
      v-for="item in cateList"
      @click="go(item.id)"
      :index="item.id"
      >{{ item.name }}</el-menu-item
    >
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router=useRouter();
const cateList: any = ref([
    {name: "Home", id: "/"},
    {name: "Control", id: "/control"}
]);
const activeIndex = ref("0");

const go=(url: string)=>{
    router.push(url);
}
</script>

<style>
.flex-grow {
  flex-grow: 1;
}
#nav {
  border: none !important;
}
.el-menu-item {
  &:hover {
    background-color: #ffffff00 !important;
  }
  --el-menu-hover-bg-color: #ffffff00 !important;
  border: none !important;
}
</style>
