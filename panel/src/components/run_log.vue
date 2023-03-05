<template>
  <div class="block">
    <el-card v-show="show" class="box-card" style="position: fixed; margin-top: 5vh; height: 85vh; margin-left: 10vw; width: 80vw;z-index: 1000; white-space: pre;overflow:auto; padding-left: 3vw;">
      <i class="el-icon-close" style="margin-left: 73vw; margin-top: 3vh; position:fixed" @click="close()"></i>
      <h3>{{ project }}于{{ time }}的运行日志</h3>
      <div>{{info}}</div>
    </el-card>
    <h3 style="font-size: xx-large; font-weight: bolder; margin-left: 3vw; margin-bottom: 3vh; margin-top: 5vh">模型训练日志</h3>
    <el-timeline style="margin-left: 3vw; width: 85vw;">
      <el-timeline-item :timestamp="log.day" placement="top" v-for="log in logs" :key="log.key">
        <el-card>
          <el-link @click="lookin(log.project, log.time)">{{log.project}}运行于{{log.time}}的日志<i class="el-icon-view el-icon--right"></i></el-link>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  <div class="mask" v-show="show"></div>
  </div>
</template>

<script>
export default {
    data(){
      return{
        info: "",
        show: false,
        logs: [],
        project: "",
        time: ""
      }
    },
    mounted(){
      this.$http.get("http://59.77.17.71:5001/getallrunlog").then(res=>{
        this.logs = res.data["logs"]
      })
    },
    methods: {
      lookin(project, time){
        this.project = project
        this.time = time
        this.$http.get("http://59.77.17.71:5001/getrunlog").then(res=>{
          this.info = res.data["log"]
          this.show = true
        })
      },
      close(){
        this.show = false
      }
    }
}
</script>
<style>
   .mask {
        display: block;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.4) no-repeat center;
    }

</style>