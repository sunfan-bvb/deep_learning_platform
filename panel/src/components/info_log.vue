<template>
  <div class="block">
    <div style="margin-left: 5vw; margin-top: 5vh;margin-bottom: 5vh;">
      <span style="font-size: xx-large; font-weight: bolder;">日志管理</span>
      <el-input v-model="input" placeholder="请输入内容" style="width: 15vw; margin-left: 2vw"></el-input>
      <el-button type="primary" icon="el-icon-search" style="margin-left: 1vh" @click="search()">搜索</el-button>
      <el-date-picker v-model="date" type="date" placeholder="选择日期" style="margin-left: 3vw;" @change="dateselect()"></el-date-picker>
      <el-button type="primary" style="margin-left: 1vh" @click="showall()">全部</el-button>
    </div>
    <el-empty description="没有相关记录" v-show="empty" :image-size="300" style="margin-top: 10vh"></el-empty>
    <el-timeline style="margin-left: 3vw; width: 85vw;" v-show="timeline">
      <el-timeline-item :timestamp="log.date" placement="top" v-for="log in show_logs" :key="log.key">
        <el-card style="margin-bottom: 2vh; font-size: medium" v-for="info in log.infos" :key="info.key">
          <h4>{{ info.op }}</h4>
          <p>{{ log.date + " " + info.time }}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        logs: [{date: '2022/8/17', infos: [{op: '登录', time: '14:12:52'}, {op: '注册', time: '14:15:52'}]},
          {date: '2022/8/18', infos: [{op: '登录', time: '14:12:52'}, {op: '注册', time: '14:15:52'}]}],
        date: '',
        input: '',
        show_logs: [{date: '2022/8/17', infos: [{op: '登录', time: '14:12:52'}, {op: '注册', time: '14:15:52'}]},
          {date: '2022/8/18', infos: [{op: '登录', time: '14:12:52'}, {op: '注册', time: '14:15:52'}]}],
        empty: false,
        timeline: true
      };
    },
    mounted(){
      this.$http.get("http://59.77.17.71:5001/getinfolog").then(res=>{
        this.logs = res.data["log"]
        this.show_logs = res.data["log"]
      })
    },
    methods:{
      dateselect(){
        let l = String(this.date).split(" ")
        let month = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        let date = l[3] + "/" + month[l[1]] + "/" + l[2]
        let flag = true
        console.log(date)
        this.logs.forEach(log=>{
          console.log(log.date)
          console.log(log.date === date)
          if(log.date === date){
            this.show_logs = [log]
            flag = false
            console.log(this.show_logs)
          }
        })
        this.empty = flag === true
        this.timeline = flag === false
        this.input = ""
      },
      showall(){
        this.show_logs = this.logs
        this.empty = false
        this.timeline = true
        this.date = ""
        this.input = ""
      },
      search(){
        this.date = ""
        let logs = []
        this.logs.forEach(log=>{
          let infos = []
          log.infos.forEach(info=>{
            console.log(info.op.indexOf(this.input))
            if(info.op.indexOf(this.input) >=0){
              infos.push(info)
            }
          })
          if(infos.length > 0){
            logs.push({"date": log.date, infos})
          }
        })
        if(logs.length > 0){
            this.show_logs = logs
        }
        this.empty = logs.length === 0
        this.timeline = logs.length > 0
      }
    }
  };
</script>