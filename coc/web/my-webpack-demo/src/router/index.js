import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'

const routerOptions = [
  {path: '/', component: 'Blank'},
  {path: '/about', component: 'About'},
  {path: '/home', component: 'Home'},
  {path: '/build_pc', component: 'BuildPc'},
  {path: '*', component: 'NotFound'}
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
//  routes: [
//    {
//      path: '/',
//      name: 'HelloWorld',
//      component: HelloWorld
//    }
//  ]
  routes,
  modes: 'history'
})
