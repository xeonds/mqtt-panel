<template>
  <el-header>
    <navBar />
  </el-header>
  <el-main>
    <router-view />
  </el-main>
  <el-footer>Powered By Vue.js</el-footer>
</template>

<script setup lang="ts">
import navBar from './components/nav-bar.vue'
</script>

<style scoped>
.el-header {
    width: 100%;
    height: 2.5rem;
}
.el-main {
    width: 100%;
    height: calc(100vh - 5rem);
}
.el-footer {
    width: 100%;
    height: 2.5rem;
}
</style>
