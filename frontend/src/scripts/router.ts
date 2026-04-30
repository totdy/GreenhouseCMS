import { createRouter, createWebHistory } from "vue-router"
import HomeView from "@/views/HomeView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/add",
      name: "add",
      component: () => import("@/views/AddHarvestView.vue"),
    },
    {
      path: "/charts",
      name: "charts",
      component: () => import("@/views/ChartsView.vue"),
    },
  ],
})

export default router
