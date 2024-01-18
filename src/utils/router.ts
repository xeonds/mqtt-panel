import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  { path: "/", component: () => import("../views/home.vue"), },
  { path: "/new", component: () => import("../views/_home.vue"), },
  { path: "/control", component: () => import("../views/control.vue"), },
];

export default createRouter({
  history: createWebHashHistory(),
  routes: routes,
});
