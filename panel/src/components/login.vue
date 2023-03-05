<template>
  <div class="body">
    <el-row>
      <el-col :span="8">
            <img src="@/assets/login.svg" alt="">
      </el-col>
      <el-col :span="16" class="login-right">
        <h1>Login</h1>
        <div style="margin-top: 5vw;">
          <el-input type="text" class="text" name="username" placeholder="用户名" v-model="name"/>
          <el-input type="password" class="text" name="password" placeholder="密码" v-model="password" style="margin-top: 3vh;"/>
        <div style="display: flex; justify-content: center">
          <span><el-button type="button" class="login" @click="toregister">注册</el-button></span>
          <span><el-button type="button" class="login" @click="login" style="margin-left: 2vw">登录</el-button></span>
        </div>
      </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {save_log} from "@/components/utils.js";
export default {
  name: "login",
  data(){
    return{
      name: "",
      password: ""
    }
  },
  methods:{
    login(){
      this.$http.post("http://59.77.17.71:5001/login", {name: this.name, password: this.password}).then(res=> {
        console.log(res)
        if(res.data !== "fail"){
          console.log(res.data)
          localStorage.setItem("token", res.data["token"])
          localStorage.setItem("role", res.data["role"])
          console.log(localStorage.getItem("token"))
          save_log("登录成功")
          this.$router.push('/projects');
        }else{
          save_log("登录失败，用户名或密码错误")
          this.$message.error("用户名或密码错误！")
        }
      })
    },
    toregister(){
      this.$router.push('/register');
    }
  }
}
</script>

<style scoped>
.body{
  width: 100vw;
  height: 100vh;
  background-color: #eaecef;
}
img{
    width: 30vw;
    height: 30vw;
    margin-top: 20vh;
    margin-left: 10vw;
}

@keyframes loading {
    0%{opacity:100;}
    50%{opacity:100;}
    80%{opacity:100;}
    100%{opacity:0;}
}

.text{
    background-color: white;
    /*border: #1b73e7 solid 5px;*/
    /*border-radius: 50px 50px 50px 50px;*/
    width: 25vw;
    display: block;
    margin-left:auto;
    margin-right:auto;
    font-size: large;
    text-align: center;
}
h1 {
    text-align: center;
    color: #3f9eff;
    font-size: 4em;
    transition: 0.5s;
    font-family: Arial, Helvetica, sans-serif;
}
h1:hover {
    text-shadow: 0 1px 0 #1b73e7, 0 2px 0 #1b73e7,
        0 3px 0 #1b73e7, 0 4px 0 #1b73e7,
        0 5px 0 #1b73e7, 0 6px 0 #1b73e7,
        0 7px 0 #1b73e7, 0 8px 0 #1b73e7,
        0 9px 0 #1b73e7, 0 10px 0 #1b73e7,
        0 11px 0 #1b73e7, 0 12px 0 #1b73e7,
        0 20px 0px rgba(0, 0, 0, 0.5);
}
.login{
    background-color: #B3DEF9;
    border: #3f9eff solid 5px;
    border-radius: 50px 50px 50px 50px;
    height: 4vw;
    width: 10vw;
    display: block;
    margin-top: 3vw;
    /*margin-left:auto;*/
    /*margin-right:auto;*/
    font-size: large;
    text-align: center;
    color: #409EFA;
    /*margin:0 auto;*/
    transition: background-color 1s;
     /* 兼容旧版Firefox */
    -moz-transition: background-color 1s;
    /* 兼容旧版Safari and Chrome */
    -webkit-transition: background-color 1s;
}
.login:hover{
    background-color: #4A4A4A;
}
.login-right{
  margin-top: 20vh;
}
</style>