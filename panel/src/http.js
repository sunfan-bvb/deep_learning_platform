import axios from 'axios';
import router from './main.js';

// axios 配置
// axios.defaults.timeout = 60 * 1000; // 1min run和test重新设置
// axios.defaults.baseURL = 'http://127.0.0.1:5000/';

// http request 拦截器
axios.interceptors.request.use(
  config => {
    if (localStorage.getItem("token")) { //判断token是否存在
      config.headers.Authorization = localStorage.getItem("token");  //将token设置成请求头
    }
    console.log(config)
    return config;
  },
  err => {
      console.log(err)
    return Promise.reject(err);
  }
);

// http response 拦截器
axios.interceptors.response.use(
  response => {
      console.log(response)
    if (response.data.errno === 999) {
      router.replace('/');
      console.log("token过期");
    }
    return response;
  },
  error => {
    return Promise.reject(error);
  }
);
export default axios;
