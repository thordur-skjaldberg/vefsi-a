import { createRouter, createWebHistory } from "vue-router";

import Forsida from "@/components/sidurnar/Forsida.vue";

const routes = [
  { path: "/", name: "forsida", component: Forsida },
  { path: "/:pathMatch(.*)*", name: "not-found", component: Forsida },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
