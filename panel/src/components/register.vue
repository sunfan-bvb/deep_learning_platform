<template>
  <div class="body">
    <el-row>
      <el-button type="text" class="back" @click="tologin" icon="el-icon-arrow-left">返回</el-button>
    </el-row>
    <el-row>
      <el-col :span="8">
            <img src="@/assets/logon.svg" alt="">
      </el-col>
      <el-col :span="16" class="login-right">
          <h1>Registration</h1>
          <div style="margin-top: 5vw;">
              <el-input type="text" class="text" name="username" placeholder="用户名" v-model="name"/>
              <el-input type="password" class="text" name="password" placeholder="密码" v-model="password"/>
              <el-button type="submit" class="login" @click="register">注册</el-button>
          </div>
      </el-col>
    </el-row>

  </div>
</template>

<script>

export default {
  name: "register",
  data(){
    return{
      name:"",
      password:""
    }
  },
  methods:{
    register(){
      this.$http.post("http://59.77.17.71:5001/register", {name: this.name, password: this.password}).then(res=> {
        console.log(res)
        if(res.data === "success"){
          this.$message({
            message: '注册成功！',
            type: 'success'
          });
          this.$router.push('/');
        }
        else if(res.data === "exist"){
          this.$message.error('用户名已存在！');
          this.name = ""
        }
      })
    },
    tologin(){
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.body{
  background-color: #eaecef;
  width: 100vw;
  height: 100vh;
}
img{
    width: 30vw;
    height: 30vw;
    margin-top: 17vh;
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
    /*border: #8541C6 solid 5px;*/
    /*border-radius: 50px 50px 50px 50px;*/
    /*height: 4vw;*/
    width: 25vw;
    display: block;
    margin-top: 3vw;
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
    margin-left:auto;
    margin-right:auto;
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
  margin-top: 17vh;
}
.back{
  margin-top: 3vh;
  margin-left: 5vw;
  font-size: medium;
}
</style>