<template>
  <el-row>
    <!--顶部工具菜单-->
    <el-col :span="24">
        <div class="ef-tooltar">
          <el-button type="text" @click="changeName" style="font-size: larger; margin-right: 1vw; color: black">{{projectName}}</el-button>
<!--          <el-button type="primary" icon="el-icon-s-home" @click="toIndex">工程面板</el-button>-->
<!--          <el-divider direction="vertical"></el-divider>-->
<!--          <el-button @click="consoleClick">控制台</el-button>-->
          <el-divider direction="vertical"></el-divider>
          <el-button @click="chartClick">图表</el-button>
          <el-divider direction="vertical"></el-divider>
          <el-button type="success" icon="el-icon-caret-right" plain @click="runAndStop">{{training?"停止训练":"开始训练"}}</el-button>
          <el-button type="success" icon="el-icon-caret-right" plain @click="pauseAndContinue" v-show="training">{{pause?"继续训练":"暂停训练"}}</el-button>
          <el-button icon="el-icon-magic-stick" @click="openDraw" type="warning" style="margin-left: 16px;"
                     plain>测试</el-button>
          <el-divider direction="vertical"></el-divider>
<!--          <el-button type="primary" @click="openChart">下载图表</el-button>-->
          <el-button type="primary" @click="saveProject('direct')">保存</el-button>
          <el-divider direction="vertical"></el-divider>
          <el-button type="primary" @click="uploadParams">上传参数</el-button>
          <el-button type="success" icon="el-icon-caret-right" plain @click="getloss">获取loss</el-button>
        </div>
    </el-col>
</el-row>
</template>

<script>
// import {jsPlumb} from "@/components/jsplumb";
import {getEnName, getNodeParams} from "@/components/data_A";
import Utils from './utils.js';
import {save_log} from "@/components/utils.js";

export default {
  name: "nav",
  data(){
    return{
      // projectName:"未命名"
      changeAble: true,
      downloadImgList: [],
      runloading: false,
      training: false,
      pause: false
    }
  },
  props:["saveParam", "data", "projectName", "epoch", "paramName", "createDate", "dataImgList", "conn", "packname", "savePre"],
  mounted() {
    let that = this
    window.setInterval(function(){
        that.saveProject("auto");
    }, 1000*300);
    Utils.$on('saveProject',()=> {
      this.saveProject("none");
    })
  },
  methods:{
    getloss(l){
      console.log(l)
      this.$http.post(
          "http://59.77.17.71:5001/visual/getloss", {project: this.projectName, l: l}
      ).then(res => {
        console.log(res.data)
        this.$emit("getLoss", res.data)
      })
    },
    toIndex(){
      this.$router.push({ name: 'projects'})
    },
    openDraw(){
      this.$emit('openDrawer')
    },
    consoleClick(){
      this.$emit('consoleClick')
    },
    chartClick(){
      this.$emit('chartClick')
    },
    openChart() {
      const h = this.$createElement;
      this.$msgbox({
        title: '下载',
        message: h('p', null, [
          h('el-button', {on:{click: () => { this.downloadLoss()},},}, '下载损失图表'),
          h('el-button', {on:{click: () => {this.downloadAcc()},},}, '下载评价函数图表')
        ]),
        showCancelButton: false,
        confirmButtonText: '确定',
      });
    },
    downloadAcc(){
      this.downloadChart("accuracy")
      return "success"
    },
    downloadLoss(){
      this.downloadChart("loss")
      return "success"
    },
    downloadChart(type){
      let l = [];
      this.data.nodeList.filter((node) => {
          let enName = getEnName(node.name);
          l.push(enName);
      })
      console.log(l);
      this.$http.post(
          "http://59.77.17.71:5001/visual/downchart",
          {type: type, project: this.projectName, l:l},
        { responseType: 'blob' }
      ).then(response => {
        if (!response) {
          return
        }
        console.log(response)
        console.log(window.URL)
        const filename = response.headers['content-disposition'].split('filename=')[1].split('; filename')[0]
        console.log(filename)
        let url = window.URL.createObjectURL(response.data)
        this.downloadImgList.push({"url":url, "name":filename})
        console.log(url)
        const link = document.createElement('a')
        link.style.display = 'none'
        link.href = url
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
      }).catch(reason => {
        console.log(reason)
        this.$message.warning(
            "暂无数据！"
        )
      })
    },
    changeName(){
      // const h = this.$createElement;
      this.$prompt('输入工程名', '提示', {
          // message: h('p', { style: 'color: red; font-size: smaller' }, "名称中请勿包含'-*-'字符串",),
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({ value }) => {
          // if(value.indexOf("-*-")>=0){
          //   this.$message.error("名称中不能包含-*-字符串！")
          // }else{
            Utils.$emit("reload")
            this.$http.post("http://59.77.17.71:5001/visual/changename", {name: value, oldname: this.projectName}).then(res=>{
            console.log(res)
             if(res.data === "success"){
               this.projectName = value;
               this.$emit("changeProjectName", value)
               save_log("修改工程名为", value)
               console.log(this.projectName)
             }else if(res.data === "exist"){
               this.$message.error("不能和现有工程名相同！")
               save_log("尝试修改工程名失败，不能和现有工程名相同！")
             }else{
               this.$message.error("新建项目请先保存再重命名！")
             }
          })
          // }
        })
    },
    getConnList(conn){
      if(conn == null){
        return []
      }
      let sources = [];
      let targets = [];
      for(let i = 0; i < conn.length; i++){
        sources.push(conn[i].sourceId)
        targets.push(conn[i].targetId)
      }
      let begin = '';
      for(let i = 0; i < sources.length; i++){
        let source = sources[i]
        for(let j = 0; j < targets.length; j++){
          if(source === targets[j]){
            break
          }
          if( j === targets.length - 1){
            begin = source;
          }
        }
      }
      let connList = [];
      connList.push(begin);
      let k = sources.indexOf(begin);
      while(k>=0){
        let target = targets[k];
        connList.push(target);
        k = sources.indexOf(target);
      }
      return connList;
    },
    getSaveParam(){
      console.log(this.saveParam)
      let type = ["保存最优参数", "保存最后一轮参数", "保存指定轮数参数", "不保存参数",""]
      let f_type = ["best", "last", "given", "nope",""]
      let index = type.indexOf(this.saveParam)
      console.log(index)
      console.log(f_type[index])
      let t = f_type[index]
      console.log(t)
      Utils.$emit("reload")
      return [t, this.epoch, this.paramName, this.savePre]
    },
    run(){
      if(this.saveParam === ""){
        this.$message.error("请选择参数保存模式！");
        return;
      }
      // let con = jsPlumb.getAllConnections();
      let connList = this.getConnList(this.conn);
      // console.log(con)
      console.log(connList)
      if(this.conn.length !== connList.length - 1){
        this.$message.error("只能有一条路径！");
        return;
      }
      // this.runloading = true
      // this.createParamFile();
      let l = [];
      let p = [];
      console.log(this.data.nodeList)
      for(let i = 0; i < connList.length; i++){
        this.data.nodeList.filter((node) => {
          console.log(node)
          if (node.id === connList[i]) {
            let enName = getEnName(node.name);
            l.push(enName);
            let params = getNodeParams(node.name)
            let param = {};
            for(var k = 0; k < params.length; k++){
              param[params[k]] = node[params[k]]
              if(params[k] === "packname"){
                param[params[k]] = this.packname
              }
            }
            p.push(param)
          }
        })
      }
      console.log(l);
      // if(l.indexOf("upload") >= 0){
      //   let newFiles = []
      //   localStorage.clear()
      //   this.dataImgList.forEach(item => {
      //   let objFile = {};
      //   objFile.title = item.name;
      //   objFile.imgFile = item.raw;
      //   newFiles.push(objFile);
      //   newFiles.forEach(image =>{
      //     var param = new FormData(); // FormData 对象
      //     var file = image.imgFile;
      //     console.log(this.packname)
      //     param.append("file", file); // 文件对象
      //     this.$http.post("http://127.0.0.1:5001/visual/upload/"+this.packname,param,
      //       {headers:{'Content-Type':'application/x-www-form-urlencoded'}}).then(res=>{
      //     console.log(res)
      //   })
      //   })
      // });
      // console.log(newFiles)
      // let i = -1
      // newFiles.forEach(fileItem => {
      //   var param = new FormData(); // FormData 对象
      //   var file = fileItem.imgFile;
      //   param.append("file", file); // 文件对象
      //   this.downloadImgList = [];
      //   i ++;
      //   this.$http.post("http://127.0.0.1:5001/visual/upload/"+i,param,
      //       {headers:{'Content-Type':'application/x-www-form-urlencoded'}}).then(res=>{
      //     console.log(res)
      //   })
      // })
      // }
      console.log(p)
      if(l.length === 0){
        this.$message.error("请先添加节点！");
        return;
      }
      let saveP = this.getSaveParam()
      this.$emit("resetLoss")
      console.log(saveP)
      let interval = ""
      // this.$http.post("http://127.0.0.1:5001/visual/getmatrix",{l: connList}).then(res=>{
      //   let matrix = res.data
      //
      // })
      interval = window.setInterval(this.getloss, 1000*2, l)
      let date = new Date()
      let time = date.toLocaleDateString() + "_" + date.toLocaleTimeString()
      this.$http.post("http://59.77.17.71:5001/visual/run",{process: l, params: p, saveP: saveP, project:this.projectName, time: time}).then(res=>{
        console.log(res);
        this.getloss(l)
        // this.runloading = false
        this.training = false
        window.clearInterval(interval)
        this.$http.post("http://59.77.17.71:5001/visual/downparam",{name: saveP[2]+".pth.tar", project: this.projectName}, { responseType: 'blob' }).then(res=>{
          console.log(res)
          const filename = res.headers['content-disposition'].split('filename=')[1].split('; filename')[0]
          console.log(filename)
          let url = window.URL.createObjectURL(res.data)
          console.log(url)
          const link = document.createElement('a')
          link.style.display = 'none'
          link.href = url
          link.setAttribute('download', filename)
          document.body.appendChild(link)
          link.click()
          this.downloadLoading = false;
          save_log("训练工程" + this.projectName)
        })
      }).catch(reason => {
        window.clearInterval(interval)
        console.log(reason)
        // this.runloading = false
        this.training = false
        this.$message.error("运行错误！请检查数据集与后续操作是否正确！")
        save_log("训练工程" + this.projectName + "发生运行错误")
      })
    },
    saveProject(save_type){
      // let con = jsPlumb.getAllConnections();
      let connList = this.getConnList(this.conn);
      console.log(connList)
      console.log(this.data.nodeList)
      let nodes = []
      this.data.nodeList.forEach(node =>{
        if(connList.indexOf(node.id) < 0){
          nodes.push(node)
        }
      })
      let p = [];
      let l = [];
      for(let i = 0; i < connList.length; i++){
        this.data.nodeList.filter((node) => {
          if (node.id === connList[i]) {
            l.push(node);
            let params = getNodeParams(node.name)
            let param = {};
            for(var k = 0; k < params.length; k++){
              param[params[k]] = node[params[k]]
            }
            p.push(param)
          }
        })
      }
      console.log(connList)
      console.log(p)
      console.log(l)
      let saveP = this.getSaveParam()
      console.log(saveP)
      let param = {params: p, nodeList: l, nodes: nodes, saveP: saveP}
      this.$http.post("http://59.77.17.71:5001/visual/save",{param: param, name: this.projectName, date: this.createDate},).then(res=>{
        if(res.data === "success"){
          console.log(save_type)
          if(save_type === "auto"){
            console.log("a")
            this.$message({message:"系统自动保存！",type:'success'})
          }
          if(save_type === "direct"){
            console.log("b")
            this.$message({message:"保存成功！",type:'success'})
            save_log("保存工程" + this.projectName)
          }
        }
      })
    },
    runAndStop(){
      console.log(this.training)
      if(this.training === false){
        this.training = true
        this.run()
      }else{
        this.$http.post("http://59.77.17.71:5001/visual/stop", {project: this.projectName}).then(res=>{
          if(res.data === "success") {
            this.training = false
            let saveP = this.getSaveParam()
            this.$http.post("http://59.77.17.71:5001/visual/downparam",{name: saveP[2]+".pth.tar", project: this.projectName}, { responseType: 'blob' }).then(res=>{
              console.log(res)
              const filename = res.headers['content-disposition'].split('filename=')[1].split('; filename')[0]
              console.log(filename)
              let url = window.URL.createObjectURL(res.data)
              console.log(url)
              const link = document.createElement('a')
              link.style.display = 'none'
              link.href = url
              link.setAttribute('download', filename)
              document.body.appendChild(link)
              link.click()
              this.downloadLoading = false;
              save_log("停止训练工程" + this.projectName)
          })
          }
        })
      }
    },
    pauseAndContinue(){
      if(this.pause === true){
        this.$http.post("http://59.77.17.71:5001/visual/continue", {project: this.projectName}).then(res=> {
          if(res.data === "success"){
            this.pause = false
            this.$message.info("训练继续")
            save_log("继续训练工程" + this.projectName)
          }
        })
      }else{
        this.$http.post("http://59.77.17.71:5001/visual/pause", {project: this.projectName}).then(res=> {
          if(res.data === "success"){
            this.pause = true
            this.$message.info("训练暂停")
            save_log("暂停训练工程" + this.projectName)
          }
        })
      }
    },
    uploadParams(){
      this.$emit("uploadParams")
    }
  }
}
</script>

<style scoped>

</style>