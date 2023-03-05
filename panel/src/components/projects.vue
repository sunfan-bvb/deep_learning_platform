<template>
  <div>
    <div>
    <div class="ef-tooltar">
      <i class="el-icon-folder-opened" style="margin-left:1vw;display: inline"></i>
      <div style="display: inline">工程面板</div>
      <el-divider direction="vertical"></el-divider>
      <el-button type="primary" icon="el-icon-circle-plus-outline" @click="toindex">新建工程</el-button>
      <el-button type="primary" icon="el-icon-circle-plus-outline" @click="topassword">修改密码</el-button>
      <el-button type="primary" icon="el-icon-user-solid" @click="toinfo" v-show="show">用户管理</el-button>
      <el-input v-model="input" placeholder="请输入内容" style="width: 15vw; margin-left: 2vw"></el-input>
      <el-button type="primary" icon="el-icon-search" style="margin-left: 1vh" @click="search">搜索</el-button>
      <el-button type="danger" icon="el-icon-switch-button" @click="logout" class="logout">登出</el-button>
    </div>
    </div>
    <el-collapse v-model="activeNames">
      <el-collapse-item name="1">
        <template slot="title">
            <h3 style="margin-left: 1vw">IDE模块面板</h3>
        </template>
        <el-row :gutter="12">
          <div v-for="code in codeList" :key="code.key">
              <el-col :span="8">
              <el-card class="box-card" shadow="hover">
              <div slot="header" class="clearfix">
                <span style="font-size: medium; font-weight: bold">{{code.name}}</span>
                <el-button style="float: right; padding: 3px 0; color: red" type="text" @click="deletecode(code.name)">删除</el-button>
              </div>
              <p>创建时间：{{code.date}}</p>
<!--              <p>修改时间：xxxx-xx-xx</p>-->
                <el-button type="primary" @click="entercode(code.name, code.date)">查看</el-button>
            </el-card>
          </el-col>
          </div>
        </el-row>
      </el-collapse-item>
      <el-collapse-item name="2">
        <template slot="title">
            <h3 style="margin-left: 1vw">模型训练模块面板</h3>
        </template>
       <el-row :gutter="12">
         <div v-for="visual in visualList" :key="visual.key">
           <el-col :span="8">
            <el-card class="box-card" shadow="hover">
              <div slot="header" class="clearfix">
                <span style="font-size: medium; font-weight: bold">{{visual.name}}</span>
                <el-button style="float: right; padding: 3px 0; color: red" type="text" @click="deletevisual(visual.name)">删除</el-button>
              </div>
              <p>创建时间：{{visual.date}}</p>
<!--              <p>修改时间：xxxx-xx-xx</p>-->
              <el-button type="primary" @click="entervisual(visual.name, visual.date)">查看</el-button>
            </el-card>
          </el-col>
         </div>
        </el-row>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script type="text/ecmascript-6">
import {save_log} from "@/components/utils.js";

export default {
  name: "projects",
  data(){
    return{
      activeNames: ['1','2'],
      codeList: [],
      visualList: [],
      jsPlumb: null,
      show: false,
      originalCodeList: [],
      originalVisualList: [],
      input: ''
    }
  },
  mounted(){
    console.log(this.show)
    this.$http.post("http://59.77.17.71:5001/getproject",{name: name}).then(res=>{
      console.log(res.data)
      this.codeList = res.data.code
      this.visualList = res.data.visual
      this.originalCodeList = this.codeList
      this.originalVisualList = this.visualList
    })
    if(this.$route.params.jsPlumb){
      this.jsPlumb = this.$route.params.jsPlumb
    }
    window.addEventListener('visibilitychange',this.reloadpage);
    this.$on('hook:beforeDestroy', () => {
      window.removeEventListener('visibilitychange', this.reloadpage)
    })
    this.$http.post("http://59.77.17.71:5001/getadmin").then(res=>{
      this.show = res.data !== 0
    })
  },
  beforeDestroy(){
    console.log("destroy");
  },
  methods:{
    reloadpage(){
      if (document.visibilityState === 'visible') {
        // this.$router.go(0)
        this.$http.post("http://59.77.17.71:5001/getproject",{name: name}).then(res=>{
          console.log(JSON.stringify(res.data.code) === JSON.stringify(this.codeList))
          if(JSON.stringify(res.data.code) !== JSON.stringify(this.originalCodeList) || JSON.stringify(res.data.visual) !== JSON.stringify(this.originalVisualList)){
            this.$router.go(0)
          }
        })
      }
    },
    entervisual(visual, date){
      const n = this.$router.resolve({ name: 'panel', query: { name: visual, createdate: date, flag: "1"}})
      window.open(n.href,visual)
    },
    toindex(){
       const n = this.$router.resolve({ name: 'index'})
      window.open(n.href)
    },
    topassword(){
      this.$router.push('/password')
    },
    toinfo(){
      this.$router.push('/infomanage')
    },
    logout(){
      this.$router.push('/')
    },
    entercode(code, date){
      this.$http.post("http://59.77.17.71:5001/code/getproject",{name: code}).then(res=>{
        // console.log(res.data)
        // this.$router.push({ name: 'code', params: { code: res.data, name: code, createdate: date}})
        const n = this.$router.resolve({ name: 'code', query: { name: code, createdate: date, code: res.data}})
        window.open(n.href, code)
      })
    },
    deletevisual(visual){
      this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$http.post("http://59.77.17.71:5001/visual/delete",{name: visual}).then(res=>{
            console.log(res.data)
            if(res.data === "success"){
              for(let i = 0; i < this.visualList.length; i++){
                if(this.visualList[i].name === visual){
                  this.visualList.splice(i, 1);
                }
              }
              // var index = this.visualList.indexOf({"name": visual, "date": date});
              this.$message({message:"删除成功！",type:'success'})
              save_log("删除可视化工程："+visual)
            }
          })
        })
    },
    deletecode(code){
      this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$http.post("http://59.77.17.71:5001/code/delete",{name: code}).then(res=>{
            console.log(res.data)
            if(res.data === "success"){
              for(let i = 0; i < this.codeList.length; i++){
                if(this.codeList[i].name === code){
                  this.codeList.splice(i, 1);
                }
              }
              this.$message({message:"删除成功！",type:'success'})
              save_log("删除IDE工程："+code)
            }
          })
        })
    },
    search(){
      let codeList = []
      let visualList = []
      this.originalCodeList.forEach(code =>{
        if(code.name.indexOf(this.input) >= 0){
          codeList.push(code)
        }
      })
      this.originalVisualList.forEach(visual =>{
        if(visual.name.indexOf(this.input) >= 0){
          visualList.push(visual)
        }
      })
      this.codeList = codeList
      this.visualList = visualList
    }
  }
}

</script>
<style scoped>
.header {
  color: #409EFA;
  height: 8vh;
  width: 100vw;
  line-height: 8vh;
  font-size: 20px;
}
.logout{
  float: right;
  margin-right: 1vw;
}
</style>