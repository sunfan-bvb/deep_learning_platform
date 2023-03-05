<template>
  <div>
    <el-drawer
        title="我是标题"
        :visible.sync="drawer"
        :before-close="handleClose"
        :with-header="false">
        <div style="margin: 2vh; overflow:auto; height:90vh">
          <div class="pic">
            <span style="margin-right: 1vw; font-size: small">选择参数</span>
            <el-select v-model="value" placeholder="请选择" style="margin-bottom: 1vh">
              <el-option
                v-for="item in options"
                :key="item.label"
                :label="item.label"
                :value="item.label">
              </el-option>
            </el-select>
          <el-upload
            ref="upload"
            class="upload-demo"
            action="http://59.77.17.71:5001/upload"
            :on-preview="handlePreview"
            :on-remove="testHandleRemove"
            :before-remove="beforeRemove"
            :on-change="testShowSuccess"
            :file-list="fileList"
            name="photo"
            multiple>
            <el-tooltip class="item" effect="dark" content="上传测试文件" placement="bottom" >
                <el-button size="small" type="primary" @click="submitUpload" >点击上传</el-button>
            </el-tooltip>
          </el-upload>
        </div>
        </div>
        <div style="display:flex; justify-content:center; align-items:center;" v-show="fileList.length!==0">
          <el-button type="primary" plain @click="test" style="float: left" :loading="loading">测试</el-button>
          <el-button type="primary" plain @click="handleDownload" style="float: left" :disabled="disabled">下载结果</el-button>
        </div>
        <el-drawer
         title="我是里面的"
         :append-to-body="true"
         :visible.sync="innerDrawer"
         :with-header="false">
          <img src="@/assets/empty.svg" alt="" v-show="downloadImgList.length===0">
          <div style="text-align: center;" v-show="downloadImgList.length===0">还没有上传图像</div>
          <div style="overflow:auto; height:90vh">
            <div v-for="img in downloadImgList" :key="img.key">
           <div style="display:flex; margin: auto">
             <img :src="img.url" alt="" style="margin: 2vh 2vh 0 2vh; height: 20vh; width: 32vh; float: left"/>
             <div style="float: left; height: 20vh; display:flex; justify-content:center; align-items:center;">{{img.name}}</div>
           </div>
         </div>
          </div>
          <el-button type="primary" plain @click="handleDownload" style="display:flex; margin: 2vh auto auto;"
                     v-show="downloadImgList.length!==0">下载结果</el-button>
       </el-drawer>
      </el-drawer>
      <el-drawer
      :size="size"
      :before-close="handleDataClose"
      :visible.sync="dataUpload"
      :with-header="false">
        <div style="margin: 2vh; overflow:auto; height: 45vh">
          <div style="margin-bottom: 2vh">请于此处上传训练集文件夹</div>
          <uploader :key="train_uploader_key" :options="train_opts" :autoStart="false" class="uploader-example"
            @file-success="onFileSuccess" @files-added="onFilesAdded" style="width: 100%">
            <uploader-unsupport></uploader-unsupport>
            <uploader-drop>
              <uploader-btn :directory="true" :single="true">选择文件夹</uploader-btn>
            </uploader-drop>
            <uploader-list></uploader-list>
          </uploader>
        </div>
        <div style="margin: 2vh; overflow:auto; height: 45vh">
          <div style="margin-bottom: 2vh">请于此处上传测试集文件夹</div>
          <uploader :key="test_uploader_key" :options="test_opts" :autoStart="false" class="uploader-example"
            @file-success="onFileSuccess" @files-added="onFilesAdded" style="width: 100%">
            <uploader-unsupport></uploader-unsupport>
            <uploader-drop>
              <uploader-btn :directory="true" :single="true">选择文件夹</uploader-btn>
            </uploader-drop>
            <uploader-list></uploader-list>
          </uploader>
        </div>
    </el-drawer>
    <el-drawer
      title="我是标题"
      :visible.sync="paramsdrawer"
      :with-header="false">
      <div style="margin-top: 3vh; text-align: center">
          <el-upload
            class="upload-demo"
            drag
            action="https://jsonplaceholder.typicode.com/posts/"
            :on-remove="onParamsRemove"
            :before-remove="beforeRemove"
            :on-change="onParamsSuccess"
            :file-list="paramList"
            multiple>
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          </el-upload>
      </div>
      <div style="display:flex; justify-content:center; align-items:center;">
        <el-button type="primary" plain @click="submitParams" style="position: fixed; bottom: 2vh;" :loading="paramloading">上传</el-button>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import JSZip from "jszip";
import axios from "axios";
import FileSaver from'file-saver'
import utils from'./utils'
const getFile = url => {
  return new Promise((resolve, reject) => {
    axios({
      method: "get",
      url,
      responseType: "arraybuffer"
      })
      .then(data => {
          resolve(data.data);
      })
      .catch(error => {
          reject("加载失败：" + error);
      });
    });
    // console.log(url)
    // axios.get(url)
    // .then(function (data) {
    //   resolve(data.data)
    // })
    // .catch(function (error) {
    //   reject("加载失败：" + error)
    // });
  // })
}

export default {
  name: "drawer",
  data(){
    return{
      // drawer: false,
      fileList: [],
      imgList: [],
      dataFileList: [],
      innerDrawer: false,
      downloadImgList: [],
      // dataUpload: false,
      options: [],
      value: '',
      train_uploader_key: new Date().getTime(),
      test_uploader_key: new Date().getTime(),
      train_opts: {
        target: 'http://59.77.17.71:5001/visual/uploaddir/train/',//SpringBoot后台接收文件夹数据的接口
        testChunks: false,//是否分片-不分片
        headers: {
          Authorization: localStorage.getItem("token")
        }
      },
      test_opts: {
        target: 'http://59.77.17.71:5001/visual/uploaddir/test/',//SpringBoot后台接收文件夹数据的接口
        testChunks: false,//是否分片-不分片
        headers: {
          Authorization: localStorage.getItem("token")
        }
      },
      dirname: "",
      size: '40vw',
      pack: "",
      loading: false,
      disabled: true,
      paramsdrawer: false,
      paramList: [],
      paramImgList: [],
      paramloading: false
    }
  },
  props:['drawer','dataUpload','projectName', 'dataImgList', "nodeList", "conn"],
  mounted() {
    console.log(this.projectName)
    console.log(this.nodeList)
    let that = this
    utils.$on('setname',(name)=> {
        that.train_opts.target='http://59.77.17.71:5001/visual/uploaddir/train/'+name
        that.test_opts.target='http://59.77.17.71:5001/visual/uploaddir/test/'+name
    })
    // this.nodeList.forEach(item=>{
    //   console.log(item)
    //   if(item.name==="本地上传"){
    //     console.log(item.packname)
    // this.train_opts.target='http://127.0.0.1:5001/visual/uploaddir/train/'+this.pack
    // this.test_opts.target='http://127.0.0.1:5001/visual/uploaddir/test/'+this.pack
      // }
    // })
  },
  methods:{
    openTest(){
      this.$http.post("http://59.77.17.71:5001/visual/gettestparam",{project: this.projectName},).then(res=>{
      res.data.params.forEach(data =>{
        if(JSON.stringify(this.options).indexOf(JSON.stringify(data)) === -1){
          this.options.push({label: data})
        }
      })
    })
    },
    testHandleRemove(file, fileList){
      this.handleRemove(file, fileList, this.fileList, this.imgList)
    },
    onParamsRemove(file, fileList){
      console.log(file, fileList)
      this.handleRemove(file, fileList, this.paramList, this.paramImgList)
    },
    dataHandleRemove(file, fileList){
      this.handleRemove(file, fileList, this.dataFileList, this.dataImgList)
      this.$emit("changeDataImgList", this.dataImgList)
    },
    handleRemove(file, fileList, l, imgl) {
      let i = 0
      imgl.forEach(f =>{
        if(f.name === file.name){
          imgl.splice(i, 1)
          l.splice(i,1)
        }
        i ++;
      })
      console.log(this.fileList)
    },
    handlePreview(file) {
      console.log(file);
    },
    beforeRemove(file, fileList){
      console.log(fileList)
        return this.$confirm(`确定移除 ${ file.name }？`);
    },
    testShowSuccess(res, file){
      this.showSuccess(res, file, this.fileList, this.imgList)
    },
    onParamsSuccess(res, file){
      this.showSuccess(res, file, this.paramList, this.paramImgList)
    },
    dataShowSuccess(res, file){
      this.showSuccess(res, file, this.dataFileList, this.dataImgList)
      this.$emit("changeDataImgList", this.dataImgList)
    },
    showSuccess(res, file, l, imgl){
      imgl.push(file[imgl.length])
      l.push({"name":res.name, "url": res.url})
      console.log(this.fileList)
    },
    submitUpload(){
      console.log("submit")
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
    test(){
      console.log("测试请求")
      this.loading = true
      let newFiles = [];
      // localStorage.clear()
      this.imgList.forEach(item => {
        let objFile = {};
        objFile.title = item.name;
        objFile.imgFile = item.raw;
        newFiles.push(objFile);
      });
      console.log(newFiles)
      let i = -1
      newFiles.forEach(fileItem => {
        var param = new FormData(); // FormData 对象
        var file = fileItem.imgFile;
        param.append("file", file); // 文件对象
        this.downloadImgList = [];
        i ++;
        console.log(this.nodeList)
        let name_l = []
        this.nodeList.forEach(item=>{
          name_l.push(item.name)
        })
        console.log(localStorage.getItem("token"))
        let token = localStorage.getItem("token")
        console.log(token)
        this.$http.post("http://59.77.17.71:5001/visual/test/"+i+"/"+this.value+"/"+this.projectName+ "/" + name_l.toString(), param,
            {headers:{'Content-Type':'application/x-www-form-urlencoded', 'Authorization': localStorage.getItem("token")}}).then(res=>{
          console.log(res)
          // const filename = res.headers['content-disposition'].split('filename=')[1].split('; filename')[0]
          let j = res.config.url.split("/visual/test")[1].split("/")[0]
          // let j = arr[arr.length - 1]
          console.log(j)
          console.log(res.data)
          this.$http.post(
              "http://59.77.17.71:5001/visual/download",
              {i: res.data, project: this.projectName},
            { responseType: 'blob' }
          ).then(response => {
            if (!response) {
              return
            }
            if(i === newFiles.length - 1){
              this.loading = false;
              this.disabled = false
              this.$message({message:"测试结束！请下载查看测试结果。", type:"success"})
            }
            // this.innerDrawer = true;
            // console.log(response)
            // console.log(window.URL)
            console.log(response)
            const filename = response.headers['content-disposition'].split('filename=')[1].split('; filename')[0]
            // console.log(filename)
            let url = window.URL.createObjectURL(response.data)
            this.downloadImgList.push({"url":url, "name":filename.split("\"")[1]})
          }).catch()
        }).catch(reason => {
          console.log(reason)
          this.loading = false;
          this.$message.error("请上传正确格式的文件！")
        });
      });
    },
    handleDownload(){
      this.downloadLoading = true;
      this.downFile()
    },
    downFile(){
       const zip = new JSZip()
       const promises = [];
       this.downloadImgList.forEach(item => {
         console.log(item.url)
         console.log(item.name)
         const promise = getFile(item.url).then(data => { // 下载文件, 并存成ArrayBuffer对象
             zip.file(item.name, data, { binary: true }) // 逐个添加文件
          })
        promises.push(promise)
         console.log(promises)
       })
       Promise.all(promises).then(() => {
         zip.generateAsync({type:"blob"}).then(content => { // 生成二进制流
           FileSaver.saveAs(content, "测试结果.zip") // 利用file-saver保存文件
         })
        });
    },
    openInner(){
      this.innerDrawer = true;
    },
    setName(name){
      this.pack = name
    },
    handleClose(){
      this.$emit("closeDraw")
    },
    handleDataClose(){
      this.$emit("closeDataDraw")
    },
    onFileSuccess: function (rootFile, file, response, chunk) {
        //这里可以根据response（接口）返回的数据处理自己的实际问题（如：从response拿到后台返回的想要的数据进行组装并显示）
        //注，这里从文件夹每上传成功一个文件会调用一次这个方法
      console.log(rootFile, file, response, chunk)
    },
    onFilesAdded(file) {
      console.log(file)
      // console.log(this.train_opts.target)
      // console.log(this.test_opts.target)
      // console.log(this.train_opts.target.split("/"))
      // let pack = this.train_opts.target.split("/")
      // console.log(pack[pack.length-1])
      // if(this.opts.target.split("/")[-1]==="") {
      //   this.$prompt('请输入包名', '提示', {
      //     confirmButtonText: '确定',
      //     cancelButtonText: '取消',
      //     inputValue: file[0].relativePath.split("/")[0]
      //   }).then(({value}) => {
      //     this.pack = value
      //     console.log(this.pack)
      //     this.$message({
      //       type: 'success',
      //       message: '设置成功'
      //     });
      //     //设置headers等参数的值
      //   })
      // }
    },
    openParams(){
      this.paramsdrawer = true
    },
    submitParams(){
      let newFiles = [];
      this.paramImgList.forEach(item => {
        let objFile = {};
        objFile.title = item.name;
        objFile.imgFile = item.raw;
        newFiles.push(objFile);
      });
      let l = []
      let i = 0
      let err_l = []
      this.paramloading = true
      newFiles.forEach(fileItem => {
        var param = new FormData(); // FormData 对象
        var file = fileItem.imgFile;
        param.append("file", file); // 文件对象
        i ++
        this.$http.post("http://59.77.17.71:5001/visual/uploadparam/"+this.projectName+ "/" + fileItem.title + "/" + i, param,
            {headers:{'Content-Type':'application/x-www-form-urlencoded', 'Authorization': localStorage.getItem("token")}}).then(res=>{
          console.log(res)
          if(res.data["state"] === "success"){
            let urls = res.config.url.split("/")
            console.log(urls)
            this.$message.success(urls[urls.length-2]+"上传成功！")
            l.push(1)
          }else{
            err_l.push(1)
            let urls = res.config.url.split("/")
            this.$message.error(urls[urls.length-2]+"上传失败！")
          }
          if(l.length + err_l.length === newFiles.length){
            this.paramloading = false
            if(l.length === newFiles.length){
              this.$message.success("上传成功！")
            }else{
              this.$message.warning(err_l.length+"个文件上传失败，请重新上传！")
            }
          }
          // const filename = res.headers['content-disposition'].split('filename=')[1].split('; filename')[0]
        }).catch(reason => {
          console.log(reason)
          this.loading = false;
          this.$message.error("请检查网络及文件格式！")
        });
      });
    }
  }
}
</script>

<style scoped>

</style>