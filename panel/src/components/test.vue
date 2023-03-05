<template>
  <div>
    <div class="title">Application</div>
    <el-row :gutter="20" style="margin-left: 3vw; margin-bottom: 1vh">
      <el-col :span="3"><div class="grid-content bg-purple">
        选择模型
      </div></el-col>
      <el-col :span="3"><div class="grid-content bg-purple">
        选择参数
      </div></el-col>
    </el-row>
    <el-row :gutter="20" style="margin-left: 3vw;  margin-bottom: 3vh">
      <el-col :span="3"><div class="grid-content bg-purple">
        <el-select v-model="project" placeholder="请选择" @change="projectChange">
          <el-option
            v-for="item in projects"
            :key="item.name"
            :label="item.name"
            :value="item.name">
          </el-option>
        </el-select>
      </div></el-col>
      <el-col :span="3"><div class="grid-content bg-purple">
        <el-select v-model="param" placeholder="请选择">
      <el-option
        v-for="item in params"
        :key="item.label"
        :label="item.label"
        :value="item.label">
      </el-option>
    </el-select>
      </div></el-col>
      <el-col :span="2"><el-button type="success" icon="el-icon-caret-right" @click="run">运行</el-button></el-col>
      <el-col :span="3"><el-button type="primary" @click="opendialog" v-show="openbtn">查看对比图</el-button></el-col>
    </el-row>
    <el-row :gutter="24" style="margin-left: 3vw; margin-bottom: 2vh">
      <el-col :span="12">
        <el-card shadow="always" :style="{height:(csv === false?'40vh': '60vh')}">
        <el-upload
          action=""
          class="avatar-uploader"
          list-type="picture-card"
          :file-list="fileList"
          :limit="limit"
          :auto-upload="false"
          :on-change="handleChange"
          :on-preview="handlePictureCardPreview"
          :on-exceed="handleExceed"
          :on-remove="handleRemove">
          <i class="el-icon-plus"></i>
        </el-upload>
        <el-dialog :visible.sync="dialogVisible">
          <img width="100%" :src="dialogImageUrl" alt="">
        </el-dialog>
        </el-card>
      </el-col>
      <el-col :span="11">
        <el-card shadow="always" :style="{height:(csv === false?'40vh': '60vh')}">
          <el-empty
              description="没有结果，请先测试。"
              :image-size="csv === false? 100:250"
              v-show="empty"
              v-loading="loading"
              element-loading-text="拼命加载中"
              element-loading-spinner="el-icon-loading"
              element-loading-background="rgba(0, 0, 0, 0.8)"></el-empty>
        <el-image
          style="height: 25vh"
          :src="url"
          fit="contain"
          :preview-src-list="[url]"
          v-show="!empty & image">
        </el-image>
        <Plotly :data="msg" style="width: 90%; height:70%;" :display-mode-bar="false"></Plotly>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog :visible.sync="dialog" :modal-append-to-body="false" custom-class="dialog">
      <img class="dialog-img" width="30%" :src="url_1" alt="">
      <img class="dialog-img" width="30%" :src="url_2" alt="">
      <img class="dialog-img" width="30%" :src="url" alt="">
    </el-dialog>
<!--    <el-row :gutter="24" style="margin-left: 3vw;">-->
<!--      <el-col :span="23">-->
<!--        <el-alert-->
<!--          title="测试成功"-->
<!--          :closable="false"-->
<!--          type="success"-->
<!--          description="结果分析"-->
<!--          show-icon>-->
<!--        </el-alert>-->
<!--      </el-col>-->
<!--    </el-row>-->
  </div>
</template>

<script>
import { Plotly } from 'vue-plotly';
import {save_log} from "@/components/utils.js";

export default {
  name: "test",
  components: {
    Plotly,
  },
  data(){
    return{
      projects: [],
      params: [],
      project: '',
      param: '',
      dialogImageUrl: '',
      dialogVisible: false,
      fileList: [],
      limit: 1,
      empty: true,
      url: "",
      loading: false,
      image: false,
      msg: "",
      csv: false,
      url_1: "",
      url_2: "",
      url_out: "",
      dialog: false,
      openbtn: false
    }
  },
  mounted() {
    this.$http.post("http://59.77.17.71:5001/getproject").then(res=>{
      this.projects = res.data.visual
    })
  },
  methods:{
    projectChange(value){
      console.log(value)
      this.empty = true
      this.msg = ""
      this.params=[]
      this.param = ""
      this.$http.post("http://59.77.17.71:5001/visual/gettestparam",{project: value},).then(res=>{
        console.log(res)
        res.data.params.forEach(data =>{
          if(JSON.stringify(this.params).indexOf(JSON.stringify(data)) === -1){
            this.params.push({label: data})
          }
        })
        console.log(this.params)
      })
      this.$http.post("http://59.77.17.71:5001/visual/gettype",{project: value}).then(res=>{
        console.log(res.data)
        this.limit = res.data.limit
        if(this.limit === 1 && this.fileList.length > 1){
          this.fileList.splice(1,1)
        }
      })
    },
    handleRemove(file) {
        console.log(file);
        for(let i=0; i < this.fileList.length; i++){
          if(file.uid === this.fileList[i].uid){
            this.fileList.splice(i,1)
          }
        }
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    handleDownload(file) {
      console.log(file);
    },
    handleChange(file){
      console.log(file)
      this.checkPhoto(file)
      let flag = true;
      this.fileList.forEach(item =>{
        if(file.uid === item.uid){
          flag = false
        }
      })
      if(flag){
        file.realurl = file.url
        if(file.raw.type === "text/csv"){
          file.url = 'https://img2.baidu.com/it/u=2101453503,339537934&fm=253&fmt=auto&app=138&f=PNG?w=500&h=500'
          this.csv = true
        }else{
          this.csv = false
        }
        if(this.fileList.length === 0){
          this.url_1 = file.realurl
        }else{
          this.url_2 = file.realurl
        }
        this.fileList.push(file)
      }
    },
    handleExceed(){
      this.$message.warning("最多只能上传一个文件！如果是变化检测等模型需要，请先选择相关模型后重新上传！")
    },
    run(){
      if(this.project === ""){
        this.$message.warning("请先选择工程及参数！")
        return
      }
      if(this.param === ""){
        this.$message.warning("请先选择参数！")
        return;
      }
      if(this.fileList.length === 0){
        this.$message.warning("请先添加文件！")
        return
      }
      this.loading = true
      this.empty = true
      const fd = new FormData();
      let l = []
      let names = []
      for(let i = 0; i < this.fileList.length; i++) {
        fd.append(this.fileList[i].name, this.fileList[i].raw);
        names.push(this.fileList[i].name.split(".")[0])
        l.push(this.fileList[i].name)
      }
      let name = ""
      if(names.length === 1){
        name = this.fileList[0].name
      }else{
        name = names.join("_")+".png"
      }
      let data = {"project": this.project, "param": this.param, "files": l}
      console.log(data)
      console.log(name)
      fd.append('data',JSON.stringify(data))
      this.$http.post('http://59.77.17.71:5001/test/run',fd,{headers:{'Content-Type':'multipart/form-data'}})
      .then(res => {
          console.log(res.data);
          this.msg = ""
          save_log("基于工程" + this.project + "测试")
          if(res.data === "csv"){
            this.csv = true
            this.$http.post('http://59.77.17.71:5001/test/figshow', {name: name, project: this.project}).then(res=> {
            console.log(res.data)
            this.loading = false;
            this.empty = false;
            this.image = false;
            this.msg = res.data;
            //  Plotly.newPlot('myDiv', res.data);}
              console.log(this.empty)
              console.log(this.csv)
              console.log(!this.empty & this.csv)
          })
          }else{
            this.csv = false;
            this.$http.post(
                "http://59.77.17.71:5001/test/down",
                {name: name, project: this.project},
              { responseType: 'blob' }
            ).then(response => {
              console.log(response)
              console.log(window.URL)
              const filename = response.headers['content-disposition'].split('filename=')[1].split('; filename')[0]
              console.log(filename)
              let url = window.URL.createObjectURL(response.data)
              console.log(url)
              this.url = url
              this.loading = false;
              this.empty = false;
              this.image = true;
              this.openbtn = true
            }).catch()
          }
      }).catch(reason => {
        console.log(reason)
        this.$message.error("运行错误！请检查文件与模型是否匹配。")
        this.loading = false;
      })
    },
    opendialog(){
      this.dialog = true
    },
    checkPhoto(file){
      console.log(file)
      console.log(file.raw)
      console.log(file.raw.type)
      let type = file.raw.type
      if(type === "image/png"){
        console.log("png")
      }else if(type === "image/jpg" || type === "image/jpeg"){
        console.log("jpeg")
      }else if(type === "image/webp"){
        console.log("bmp")
      }else if(type === "text/csv"){
        console.log("csv")
      }else if(type === "video/mp4"){
        console.log("mp4")
      }else if(type === "video/divx"){
        console.log("divx")
      }else if(type === "video/mp4"){
        console.log("mp4")
      }
    }
  }
}
</script>

<style scoped>
 .title{
      text-align: center;
      padding-top: 2.5vh;
      padding-bottom: 2.5vh;
      color: #2417ff;
      font-size: 10vh;
      width: 80vw;
      margin-left: 10vw;
      border-radius: 0px 0px 50px 50px;
      background-color: white;
  }
 .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
  /deep/.dialog{
    height: 70vh;
    width: 90vw;
  }
  .dialog-img{
    margin-left: 2.5%;
  }
</style>
