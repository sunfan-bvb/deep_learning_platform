import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '@/components/index.css'
import ECharts from "vue-echarts";
import VueRouter from 'vue-router'
import panel from "@/components/panel";
import index from "@/components/index";
import code from "@/components/code"
import manage from "@/components/manage"
// import axios from 'axios'
// import VueAxios from 'vue-axios'
import login from "@/components/login"
import register from "@/components/register"
import projects from "@/components/projects";
import uploader from 'vue-simple-uploader'
import test from '@/components/test'
import http from './http';  //此处问http文件的路径
import InfoManage from "@/components/InfoManage";
import password from "@/components/password"
import infolog from "@/components/info_log"
import runlog from "@/components/run_log"

Vue.prototype.$http = http;
Vue.config.productionTip = false

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(ElementUI, {size: 'small'})
Vue.use(ECharts)
Vue.use(VueRouter)
// Vue.use(VueAxios, axios)
Vue.use(uploader)
Vue.prototype.$bus = new Vue()

const router = new VueRouter({
  routes:[{
    path: '/panel',
    name: 'panel',
    component: panel,
    meta: {
        requireAuth: false // 标识该路由是否需要登录
    }
  },
    {
    path: '/',
    component: login,
        meta: {
        requireAuth: false // 标识该路由是否需要登录
    }
  },
    {
      path: '/code',
      name: 'code',
      component: code,
        meta: {
        requireAuth: true // 标识该路由是否需要登录
      }
    },
    {
      path: '/index',
      name: 'index',
      component: index,
        meta: {
        requireAuth: true // 标识该路由是否需要登录
      }
    },
    {
      path: '/register',
      name: 'register',
      component: register,
        meta: {
        requireAuth: false // 标识该路由是否需要登录
      }
    },
    {
      path: '/projects',
      name: 'projects',
      component: projects,
        meta: {
        requireAuth: true // 标识该路由是否需要登录
      }
    },
    {
      path: '/test',
      name: 'test',
      component: test,
        meta: {
        requireAuth: false // 标识该路由是否需要登录
      }
    },
      {
          path: '/infomanage',
          name: 'infomanage',
          component: InfoManage,
          meta: {
              requireAuth: true
          }
      },
      {
          path: '/password',
          name: 'password',
          component: password,
          meta: {
              requireAuth: true
          }
      },
      {
          path: '/manage',
          name: 'manage',
          component: manage,
          meta: {
              requireAuth: true
          }
      },
      {
          path: '/infolog',
          name: 'infolog',
          component: infolog,
          meta: {
              requireAuth: true
          }
      },
      {
          path: '/runlog',
          name: 'runlog',
          component: runlog,
          meta: {
              requireAuth: true
          }
      },
  ]
})

router.beforeEach((to, from, next) => {
    if (to.matched.some((auth) => auth.meta.requireAuth)) {
        let token = localStorage.getItem("token");
        if (token) {
            next();
        } else {
            next({
                path: "/"
            });
        }
    } else {
        next();
    }
})
new Vue({
  el:"#app",
  router,
  render: h => h(App),
}).$mount('#app')
