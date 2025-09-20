import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import TheWelcome from '../components/TheWelcome.vue'
import NotFound from '../components/NotFound.vue'

const routes = [
  { path: '/', name: 'home', component: HelloWorld },
  { path: '/about', name: 'about', component: TheWelcome },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound } // almenn 404 síða
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
