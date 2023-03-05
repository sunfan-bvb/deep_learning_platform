<template>
    <div v-if="easyFlowVisible" style="height: calc(100vh);">
      <el-row>
            <!--顶部工具菜单-->
            <el-col :span="24">
                <div class="ef-tooltar">
                  <el-button type="primary" icon="el-icon-s-home" @click="toIndex">首页</el-button>
                  <el-divider direction="vertical"></el-divider>
                  <el-button @click="consoleClick">控制台</el-button>
                  <el-divider direction="vertical"></el-divider>
                  <el-button @click="chartClick">图表</el-button>
                  <el-divider direction="vertical"></el-divider>
                  <el-button type="success" icon="el-icon-caret-right" plain @click="run">训练</el-button>
                  <el-button icon="el-icon-magic-stick" @click="drawer = true" type="warning" style="margin-left: 16px;"
                             plain>测试</el-button>
                  <el-divider direction="vertical"></el-divider>
                  <el-button type="primary" @click="openChart">下载图表</el-button>
                </div>
            </el-col>
        </el-row>
      <el-drawer
        title="我是标题"
        :visible.sync="drawer"
        :with-header="false">
        <div style="margin: 2vh; overflow:auto; height:90vh">
          <div class="pic">
          <el-upload
            ref="upload"
            class="upload-demo"
            action="http://localhost:8080/upload"
            :on-preview="handlePreview"
            :on-remove="testHandleRemove"
            :before-remove="beforeRemove"
            :on-change="testShowSuccess"
            :file-list="fileList"
            name="photo"
            list-type="picture"
            multiple>
            <el-tooltip class="item" effect="dark" content="大小不超过500kb" placement="bottom" >
                <el-button size="small" type="primary" @click="submitUpload" >点击上传</el-button>
            </el-tooltip>
          </el-upload>
        </div>
        </div>
        <div style="display:flex; justify-content:center; align-items:center;" v-show="fileList.length!==0">
          <el-button type="primary" plain @click="test" style="float: left">测试</el-button>
          <el-button type="primary" plain @click="openInner" style="float: left">查看结果</el-button>
        </div>
        <el-drawer
         title="我是里面的"
         :append-to-body="true"
         :before-close="handleClose"
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
          <el-button type="primary" plain @click="handleDownload" style="display:flex; margin: auto; margin-top: 2vh;"
                     v-show="downloadImgList.length!==0">下载结果</el-button>
       </el-drawer>
      </el-drawer>
        <div style="display: flex;height: calc(100% - 47px);">
            <div style="width: 230px; height: 94vh; overflow-y:scroll; overflow-x: hidden; border-right: 1px solid #dce3e8;">
                <node-menu @addNode="addNode" @getSaveParam="getSaveParam" ref="nodeMenu"></node-menu>
            </div>
            <div id="efContainer" ref="efContainer" class="container" v-flowDrag>
                <template v-for="node in data.nodeList">
                    <flow-node
                        ref="flowNode"
                      :id="node.id"
                      :key="node.id"
                      :node="node"
                      :activeElement="activeElement"
                      @clickNode="clickNode"
                    >
                    </flow-node>
                </template>
                <div style="position: fixed; bottom: 0px; height: 30%; width: 100%; z-index: 101;" v-show="isShow">
                  <el-tabs v-model="activeName" type="border-card" style="height: 100%; width: 100%">
                  <el-tab-pane label="控制台" name="console">{{message}}</el-tab-pane>
                </el-tabs>
                </div>
                <div style="position: fixed; bottom: 0px; height: 50%; width: 100%; z-index: 101;" v-show="chartIsShow">
                    <el-tabs v-model="activeNameC" type="border-card" style="height: 100%; width: 100%">
                      <el-tab-pane label="图表" name="chart" id="chart" style="height: 100%; width: 100%;">
                        <div style="display: inline-block;">
                          <div class="chart" ref="line" id="line1" style="height:350px; width: 500px; float: left"></div>
                          <div style="background-color: #565758; height: 300px; width: 1px; float: left; margin: 15px 15px 15px 15px;"></div>
                          <div class="chart" ref="line" id="line2" style="height:350px; width: 500px; float: left"></div>
                        </div>
                      </el-tab-pane>
                    </el-tabs>
                  </div>
                <div style="position:absolute;top: 2000px;left: 2000px;">&nbsp;</div>
            </div>
            <div style="width: 300px;border-left: 1px solid #dce3e8;background-color: #FBFBFB; z-index: 100;">
                <flow-node-form ref="nodeForm" @openDataUpload="openDataUpload" @changePackageName="changePackageName"></flow-node-form>
            </div>
        </div>
      <div class="pic">
        <el-drawer
        title="我是标题"
        :visible.sync="dataUpload"
        :with-header="false">
        <el-upload
          class="upload-demo"
          action="http://localhost:8080/upload"
          :on-preview="handlePreview"
          :on-remove="dataHandleRemove"
          :before-remove="beforeRemove"
          :on-change="dataShowSuccess"
          multiple
          :file-list="dataFileList">
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
        </el-upload>
      </el-drawer>
      </div>
    </div>

</template>

<script>

import './jsplumb'
import {easyFlowMixin} from '@/components/mixins'
import flowNode from '../components/node'
import nodeMenu from '../components/node_menu'
import FlowNodeForm from '../components/node_form'
import lodash from 'lodash'
import {jsPlumb} from "@/components/jsplumb";
import {getData, getDataA, getEnName, getNodeParams} from "@/components/data_A";
import JSZip from'jszip'
import FileSaver from'file-saver'
import axios from "axios";


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
}

export default {
      data() {
        return {
          // jsPlumb 实例
          jsPlumb: null,
          // 控制画布销毁
          easyFlowVisible: true,
          // 控制流程数据显示与隐藏
          flowInfoVisible: false,
          // 是否加载完毕标志位
          loadEasyFlowFinish: false,
          flowHelpVisible: false,
          // 数据
          data: {},
          // 激活的元素、可能是节点、可能是连线
          activeElement: {
            // 可选值 node 、line
            type: undefined,
            // 节点ID
            nodeId: undefined,
            // 连线ID
            sourceId: undefined,
            targetId: undefined
          },
          zoom: 0.5,
          isShow: false,
          activeName: "console",
          activeNameC: "chart",
          consoleType: "",
          message: "显示控制台信息",
          chartIsShow: false,
          drawer: false,
          fileList: [],
          imgList: [],
          dataFileList: [],
          dataImgList: [],
          saveParam: "",
          epoch: 100,
          downloadLoading:false,
          innerDrawer: false,
          downloadImgList: [],
          i: 0,
          dataUpload: false,
          packname: ""
        }
      },
      // 一些基础配置移动该文件中
      mixins: [easyFlowMixin],
      components: {
        flowNode, nodeMenu, FlowNodeForm
      },
      directives: {
        'flowDrag': {
          bind(el, binding) {
            if (!binding) {
              return
            }
            el.onmousedown = (e) => {
              if (e.button === 2) {
                // 右键不管
                return
              }
              //  鼠标按下，计算当前原始距离可视区的高度
              let disX = e.clientX
              let disY = e.clientY
              el.style.cursor = 'move'

              document.onmousemove = function (e) {
                // 移动时禁止默认事件
                e.preventDefault()
                const left = e.clientX - disX
                disX = e.clientX
                el.scrollLeft += -left

                const top = e.clientY - disY
                disY = e.clientY
                el.scrollTop += -top
              }

              document.onmouseup = function () {
                el.style.cursor = 'auto'
                document.onmousemove = null
                document.onmouseup = null
              }
            }
          }
        }
      },
      mounted() {
        this.jsPlumb = jsPlumb.getInstance()
        this.$nextTick(() => {
          // 默认加载流程A的数据、在这里可以根据具体的业务返回符合流程数据格式的数据即可
          this.dataReload()
        })
      },
      methods: {
        // 返回唯一标识
        getUUID() {
          return Math.random().toString(36).substr(3, 10)
        },
        jsPlumbInit() {
          this.easyFlowVisible = false
          this.data.nodeList = []
          this.data.lineList = []
          this.$nextTick(() => {
            this.easyFlowVisible = true
          })
          this.jsPlumb.ready(() => {
            // 导入默认配置
            this.jsPlumb.importDefaults(this.jsplumbSetting)
            jsPlumb.bind('click', function (conn) {
              let r = confirm("确定删除连线吗？");
              if (r === true) {
                jsPlumb.deleteConnection(conn);
              }
            });
            jsPlumb.bind("connection", function (conn) {
              if (conn.sourceId === conn.targetId) {
                alert("不能连接本身节点！");
                jsPlumb.deleteConnection(conn.connection)
              }
            });
            let that = this;
            jsPlumb.bind('endpointClick', function (conn) {
              var data = getData(conn.element.innerText, conn.anchor.x, conn.anchor.y);
              that.$message(data);
            })
            // 会使整个jsPlumb立即重绘。
            this.jsPlumb.setSuspendDrawing(false, true);
          })
        },
        /**
         * 拖拽结束后添加新的节点
         * @param evt
         * @param nodeMenu 被添加的节点对象
         * @param mousePosition 鼠标拖拽结束的坐标
         */
        addNode(evt, nodeMenu) {
          console.log(nodeMenu)
          var screenX = evt.originalEvent.clientX, screenY = evt.originalEvent.clientY
          let efContainer = this.$refs.efContainer
          var containerRect = efContainer.getBoundingClientRect()
          var left = screenX, top = screenY
          // 计算是否拖入到容器中
          if (left < containerRect.x || left > containerRect.width + containerRect.x || top < containerRect.y || containerRect.y > containerRect.y + containerRect.height) {
            this.$message.error("请把节点拖入到画布中")
            return
          }
          left = left - containerRect.x + efContainer.scrollLeft
          top = top - containerRect.y + efContainer.scrollTop
          // 居中
          left -= 85
          top -= 16
          var nodeId = this.getUUID()
          console.log(nodeId)
          // 动态生成名字
          var origName = nodeMenu.name
          var nodeName = origName
          var index = 1
          while (index < 10000) {
            var repeat = false
            for (var i = 0; i < this.data.nodeList.length; i++) {
              let node = this.data.nodeList[i]
              if (node.name === nodeName) {
                nodeName = origName + index
                repeat = true
              }
            }
            if (repeat) {
              index++
              continue
            }
            break
          }
          console.log(index)
          var node = {
            id: nodeId,
            name: nodeName,
            type: nodeMenu.type,
            left: left + 'px',
            top: top + 'px',
            ico: nodeMenu.ico,
            state: 'success',
            show: true
          }
          console.log(node)
          /**
           * 这里可以进行业务判断、是否能够添加该节点
           */
          this.data.nodeList.push(node)
          console.log(this.data.nodeList)
          console.log(this.jsPlumb)
          this.$forceUpdate()
          this.$nextTick(function () {
            this.jsPlumb.makeSource(nodeId, lodash.merge(this.jsplumbSourceOptions, {}))
            this.jsPlumb.makeTarget(nodeId, this.jsplumbTargetOptions)
            let baseStyle = {
              endpoint: ['Dot', {
                radius: 8,
                fill: 'white'
              }], // 端点的形状
              paintStyle: {
                strokeStyle: '#1e8151',
                stroke: '#7AB02C',
                fill: 'white',
                fillStyle: '#1e8151',
                radius: 6,
                lineWidth: 2
              },
              hoverPaintStyle: {stroke: 'orange'},
              connector: ['StateMachine'],  // 连接线的样式种类有[Bezier],[Flowchart],[StateMachine ],[Straight ]
              connectorStyle: {stroke: '#071925' ,lineWidth: 2},
              maxConnections: -1, // 设置连接点最多可以连接几条线
              connectorOverlays: [
                ['Arrow', {
                  width: 10,
                  length: 10,
                  location: 1
                }],
              ],
              connectorHoverStyle:{stroke:'orange'}
            }
            let data_A = getDataA();
            for(let i = 0; i<data_A.nodeList.length; i++){
              let data = data_A.nodeList[i];
              if(nodeName.indexOf(data.name) !== -1){
                for(let j = 0; j<data.anchors.length; j++){
                  if(data.anchors[j].indexOf("Top") !== -1){
                    jsPlumb.addEndpoint(nodeId, {
                      anchor: data.anchors[j],
                      uuid: nodeId + data.names[j],
                      isSource: false,
                      isTarget: true
                    }, baseStyle)
                  }else{
                    jsPlumb.addEndpoint(nodeId, {
                      anchor: data.anchors[j],
                      uuid: nodeId + data.names[j],
                      isSource: true,
                      isTarget: false
                    }, baseStyle)
                  }
                }
                break;
              }
            }
            this.jsPlumb.setSuspendDrawing(false, true);
            this.jsPlumb.draggable(nodeId, {
              containment: 'parent',
              drag: function () {
                jsPlumb.repaintEverything();
              },
              stop: function (el) {
                console.log('拖拽结束: ', el)
              }
            })
          })
        },
        clickNode(nodeId) {
          this.activeElement.type = 'node'
          this.activeElement.nodeId = nodeId
          this.$refs.nodeForm.nodeClick(this.data, nodeId)
        },
        dataReload() {
          this.easyFlowVisible = false
          this.data.nodeList = []
          this.data.lineList = []
          this.$nextTick(() => {
            this.easyFlowVisible = true
            this.$nextTick(() => {
              this.jsPlumb = jsPlumb.getInstance()
              this.$nextTick(() => {
                this.jsPlumbInit()
              })
            })
          })
        },
        deleteNode(nodeId) {
          this.$confirm('确定要删除节点' + nodeId + '?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
            closeOnClickModal: false
          }).then(() => {
            jsPlumb.remove(nodeId);
            this.$nextTick(function () {
              this.jsPlumb.removeAllEndpoints(nodeId);
            })
          }).catch(() => {
          })
          return true
        },
        repaintEverything() {
          this.jsPlumb.repaintEverything();
        },
        consoleClick() {
          if(this.chartIsShow){
            this.isShow = true;
            this.chartIsShow = false;
          }else{
            this.isShow = !this.isShow;
          }
        },
        chartClick() {
          this.chartIsShow = !this.chartIsShow;
          if(this.chartIsShow){
            this.getLine();
          }
        },
        getLine() {
          const echarts = require('echarts');
          require('echarts-gl');
          let myChart1 = echarts.init(document.getElementById("line1"), 'light');
          let myChart2 = echarts.init(document.getElementById("line2"), 'light');
          // 指定图表的配置项和数据
          // option将要设置以下字段感觉就足够使用了
          let option= {
            legend: {
                data: ['训练集准确率', '测试集准确率']
            },
            xAxis: {
              type: 'category',   // 还有其他的type，可以去官网喵两眼哦
              data: [500, 1000, 1500, 2000, 2500, 3000, 3500],   // x轴数据
              name: 'epoch',   // x轴名称
              // x轴名称样式
              nameTextStyle: {
                fontWeight: 100,
                fontSize: 12}
            },
            yAxis: {
              type: 'value',
              name: '准确率',   // y轴名称
              // y轴名称样式
              nameTextStyle: {
                fontWeight: 100,
                fontSize: 12
              }
            },
            label: {},
            tooltip: {
              trigger: 'axis'   // axis   item   none三个值
            },
            series: [
                {
                  name: '训练集准确率',
                  data: [820, 932, 967, 1007, 1290, 1330, 1320],
                  type: 'line'
                },
                {
                  name: '测试集准确率',
                  data: [620, 711, 823, 934, 987, 1067, 1178],
                  type: 'line'
                }
            ]
          }
          let loss_option= {
            legend: {
                data: ['训练集loss', '测试集loss']
            },
            xAxis: {
              type: 'category',   // 还有其他的type，可以去官网喵两眼哦
              data: [500, 1000, 1500, 2000, 2500, 3000, 3500],   // x轴数据
              name: 'epoch',   // x轴名称
              // x轴名称样式
              nameTextStyle: {
                fontWeight: 100,
                fontSize: 12}
            },
            yAxis: {
              type: 'value',
              name: 'loss',   // y轴名称
              // y轴名称样式
              nameTextStyle: {
                fontWeight: 100,
                fontSize: 12
              }
            },
            label: {},
            tooltip: {
              trigger: 'axis'   // axis   item   none三个值
            },
            series: [
                {
                  name: '训练集loss',
                  data: [1200, 999, 789, 567, 453, 320, 234],
                  type: 'line'
                },
                {
                  name: '测试集loss',
                  data: [1321, 1234, 1190, 1160, 1140, 920, 612],
                  type: 'line'
                }
            ]
          }
          myChart1.setOption(option);
          myChart1.resize();
          myChart2.setOption(loss_option);
          myChart2.resize();
        },
        toIndex(){
          this.$router.push('/');
        },
        run(){
          if(this.saveParam === ""){
            this.$message.error("请选择参数保存模式！");
            return;
          }
          let con = jsPlumb.getAllConnections();
          let connList = this.getConnList(con);
          console.log(con)
          console.log(connList)
          if(con.length !== connList.length - 1){
            this.$message.error("只能有一条路径！");
            return;
          }
          let l = [];
          let p = [];
          for(let i = 0; i < connList.length; i++){
            this.data.nodeList.filter((node) => {
              if (node.id === connList[i]) {
                let enName = getEnName(node.name);
                l.push(enName);
                let params = getNodeParams(node.name)
                let param = {};
                for(var k = 0; k < params.length; k++){
                  param[params[k]] = node[params[k]]
                }
                p.push(param)
              }
            })
          }
          console.log(l);
          if(l.indexOf("upload") >= 0){
            let newFiles = []
            localStorage.clear()
            this.dataImgList.forEach(item => {
            let objFile = {};
            objFile.title = item.name;
            objFile.imgFile = item.raw;
            newFiles.push(objFile);
            newFiles.forEach(image =>{
              var param = new FormData(); // FormData 对象
              var file = image.imgFile;
              console.log(this.packname)
              param.append("file", file); // 文件对象
              this.$http.post("http://59.77.17.71:5001/visual/upload/"+this.packname,param,
                {headers:{'Content-Type':'application/x-www-form-urlencoded'}}).then(res=>{
              console.log(res)
            })
            })

          });
          console.log(newFiles)
          let i = -1
          newFiles.forEach(fileItem => {
            var param = new FormData(); // FormData 对象
            var file = fileItem.imgFile;
            param.append("file", file); // 文件对象
            this.downloadImgList = [];
            i ++;
            this.$http.post("http://59.77.17.71:5001/visual/upload/"+i,param,
                {headers:{'Content-Type':'application/x-www-form-urlencoded'}}).then(res=>{
              console.log(res)
            })
          })
          }
          console.log(p)
          if(l.length === 0){
            this.$message.error("请先添加节点！");
            return;
          }
          this.$http.post("http://59.77.17.71:5001/visual/run",{process: l, params: p}).then(res=>{
            console.log(res);
            this.$http.post("http://59.77.17.71:5001/visual/downparam",{name: "best_model.h5"}, { responseType: 'blob' }).then(res=>{
              console.log(res)
              const filename = res.headers['content-disposition'].split('filename=')[1].split('; filename')[0]
                console.log(filename)
                let url = window.URL.createObjectURL(res.data)
                console.log(url)
                const link = document.createElement('a')
                link.style.display = 'none'
                link.href = url
                link.setAttribute('download', '参数' + filename)
                document.body.appendChild(link)
                link.click()
                this.downloadLoading = false;
            })
          });
        },
        testHandleRemove(file, fileList){
          this.handleRemove(file, fileList, this.fileList, this.imgList)
        },
        dataHandleRemove(file, fileList){
          this.handleRemove(file, fileList, this.dataFileList, this.dataImgList)
        },
        handleRemove(file, fileList, l, imgl) {
          l = fileList
          let i = 0
          imgl.forEach(f =>{
            if(f.name === file.name){
              imgl.splice(i, 1)
            }
            i ++;
          })
        },
        handlePreview(file) {
          console.log(file);
        },
        rewriteNodeList(nodeList){
          this.data.nodeList = nodeList
        },
        getConnList(conn){
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
        getSaveParam(saveParam, epoch){
          this.saveParam = saveParam;
          this.epoch = epoch;
        },
        beforeRemove(file, fileList){
          console.log(fileList)
            return this.$confirm(`确定移除 ${ file.name }？`);
        },
        testShowSuccess(res, file){
          this.showSuccess(res, file, this.fileList, this.imgList)
        },
        dataShowSuccess(res, file){
          this.showSuccess(res, file, this.dataFileList, this.dataImgList)
        },
        showSuccess(res, file, l, imgl){
          imgl.push(file[imgl.length])
          l.push({"name":res.name, "url": res.url})
        },
        // //这个函数貌似没用
        submitUpload(){
          console.log("submit")
        },
        test(){
          console.log("测试请求")
          let newFiles = [];
          localStorage.clear()
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
            this.$http.post("http://59.77.17.71:5001/visual/test/"+i,param,
                {headers:{'Content-Type':'application/x-www-form-urlencoded'}}).then(res=>{
              console.log(res)
              // const filename = res.headers['content-disposition'].split('filename=')[1].split('; filename')[0]
              let arr = res.config.url.split("/")
              let j = arr[arr.length - 1]
              this.$http.post(
                  "http://59.77.17.71:5001/visual/download",
                  {i: j},
                { responseType: 'blob' }
              ).then(response => {
                if (!response) {
                  return
                }
                this.innerDrawer = true;
                console.log(response)
                console.log(window.URL)
                const filename = response.headers['content-disposition'].split('filename=')[1].split('; filename')[0]
                console.log(filename)
                let url = window.URL.createObjectURL(response.data)
                this.downloadImgList.push({"url":url, "name":filename.split("\"")[1]})
              }).catch()
            });
          });
        },
        handleDownload(){
          this.downloadLoading = true;
          this.downFile()
        },
        openInner(){
          this.innerDrawer = true;
        },
        downFile(){
           const zip = new JSZip()
           const promises = [];
           this.downloadImgList.forEach(item => {
                const promise = getFile(item.url).then(data => { // 下载文件, 并存成ArrayBuffer对象
                 zip.file(item.name, data, { binary: true }) // 逐个添加文件
              })
            promises.push(promise)
           })
           Promise.all(promises).then(() => {
             zip.generateAsync({type:"blob"}).then(content => { // 生成二进制流
               FileSaver.saveAs(content, "测试结果.zip") // 利用file-saver保存文件
             })
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
          this.$http.post(
              "http://59.77.17.71:5001/visual/downchart",
              {type: type},
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
            this.downloadImgList.push({"url":url, "name":filename.split("\"")[1]})
            console.log(url)
            const link = document.createElement('a')
            link.style.display = 'none'
            link.href = url
            link.setAttribute('download', filename)
            document.body.appendChild(link)
            link.click()
          }).catch()
        },
        openChart() {
          const h = this.$createElement;
          this.$msgbox({
            title: '下载',
            message: h('p', null, [
              h('el-button', {on:{click: () => { this.downloadLoss()},},}, '下载损失图表'),
              h('el-button', {on:{click: () => {this.downloadAcc()},},}, '下载准确率图表')
            ]),
            showCancelButton: false,
            confirmButtonText: '确定',
          });
        },
        openDataUpload(){
          this.dataUpload = true
        },
        changePackageName(packname){
          this.packname = packname
          console.log(this.packname)
        }
      },
    }
</script>
