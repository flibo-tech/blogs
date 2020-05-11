import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Article from "../views/Article.vue";
import Meta from "vue-meta";

Vue.use(VueRouter);
Vue.use(Meta);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/:content_name_piece",
    name: "Article",
    component: Article,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
