<template>
  <div>
    <div class="el-icon-back" style="margin-top: 5vh; margin-left: 5vw; color: #1b73e7; font-size: 2vh;" @click="back()"><span style="font-size: 2vh">返回</span></div>
    <el-card class="box-card" style="width: 40%; height: 60vh; margin-top: 5vh; margin-left: 30vw; text-align: center">
      <h2 style="color: #1b73e7; margin-bottom: 5vh">修改密码</h2>
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="旧密码" label-width="100px" style="margin-bottom: 5vh">
          <el-input v-model="form.old"></el-input>
        </el-form-item>
        <el-form-item label="新密码" label-width="100px" style="margin-bottom: 5vh">
          <el-input v-model="form.new"></el-input>
        </el-form-item>
        <el-form-item label="新密码验证" label-width="100px" style="margin-bottom: 15vh">
          <el-input v-model="form.valid"></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="submit()">提交</el-button>
    </el-card>
  </div>
</template>

<script type="text/ecmascript-6">
import {save_log} from "@/components/utils.js";

export default {
  data(){
    return{
      form:{
        old: '',
        new: '',
        valid: ''
      }
    }
  },
  methods:{
    submit(){
      if(this.form.new !== this.form.valid){
        this.$message.error("两次密码输入不同！")
      }else if(this.form.new === ''){
        this.$message.error("密码不能为空！")
      }else{
        this.$http.post("http://59.77.17.71:5001/updatepassword", {new: this.form.new, old: this.form.old}).then(res=>{
            if(res.data === "password error"){
              this.$message.error("原密码错误！")
              save_log("尝试修改密码但原密码输入错误")
            }else if(res.data === "success"){
              this.$message.success("修改成功！")
              save_log("修改密码成功")
            }
        })
      }
    },
    back(){
      if (window.history.length <= 1) {
        this.$router.push('/projects')
        return false;
      } else {
        this.$router.go(-1);
      }
    }
  }
}

</script>
<style scoped>

</style>