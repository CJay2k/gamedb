import { createRouter, createWebHistory } from "vue-router";
// import Home from "@/views/Home.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: '/search',
      name: "home",
      // component: Home,
    },
    {
      path: "/search",
      name: "search",
      component: () => import("@/views/Search.vue"),
    },
    {
      path: "/game/:slug",
      name: "game",
      component: () => import("@/views/GameDetails.vue"),
    },

  ],
});

export default router;
