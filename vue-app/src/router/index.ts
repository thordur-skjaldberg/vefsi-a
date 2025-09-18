// src/router/index.ts
import { createRouter, createWebHistory } from "vue-router";

import Forsida from "@/components/siðurnar/forsida.vue";
import Kort from "@/components/siðurnar/Kort.vue";
import Samanburdur from "@/components/siðurnar/samanburdur.vue";
import User from "@/components/siðurnar/user.vue";

const routes = [
  { path: "/", name: "forsida", component: Forsida },
  { path: "/kort", name: "kort", component: Kort },
  { path: "/samanburdur", name: "samanburdur", component: Samanburdur },
  { path: "/user", name: "user", component: User },
  // Fallback: sendum allt óþekkt á forsíðu (má breyta í 404 síðu síðar)
  { path: "/:pathMatch(.*)*", name: "not-found", redirect: "/" },
];

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
