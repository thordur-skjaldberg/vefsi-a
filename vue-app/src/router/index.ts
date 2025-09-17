import { createRouter, createWebHistory } from "vue-router";

// TEMP: inline component to prove the router uses this file
const ForsidaTEST = {
  template: '<div style="padding:1rem"><h1>Forsíða TEST</h1></div>',
};

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "home", component: ForsidaTEST }, // <- must show "Forsíða TEST"
    {
      path: "/about",
      name: "about",
      component: { template: "<div>About</div>" },
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: { template: "<div>404 – Síða fannst ekki</div>" },
    },
  ],
});

export default router;
