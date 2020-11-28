import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/components/navs/Home.vue'
import Homes from '@/views/Home.vue'
import URLPage from '@/views/URLPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    children: [
      {
        path: 'photo',
        name: 'Home',
        component: Homes,
      },
      {
        path: 'url',
        name: 'URL',
        component: URLPage,
      }
    ]
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/About.vue')
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
