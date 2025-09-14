import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import TheWelcome from '../components/TheWelcome.vue' 

const routes = [
  { path: '/', name: 'home', component: HelloWorld },
  { path: '/about', name: 'about', component: TheWelcome }, 
  { path: '/:pathMatch(.*)*', name: 'not-found', component: HelloWorld } //hálfgert 404? vantar meira... 
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
