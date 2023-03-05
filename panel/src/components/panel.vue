<template>
    <div v-show="easyFlowVisible" style="height: calc(100vh);">
      <navi ref="nav" @openDrawer="openDrawer" @consoleClick="consoleClick" @chartClick="chartClick" :saveParam="saveParam" :projectName="projectName"
            :data="data" :epoch="epoch" :paramName="paramName" :createDate="createDate" :dataImgList="dataImgList" :conn="conn" :savePre="savePre"
            :packname="packname" @getLoss="getLoss" @resetLoss="resetLoss" @changeProjectName="changeProjectName" @uploadParams="uploadParams"></navi>
        <div style="display: flex;height: calc(100% - 47px);">
            <div style="width: 230px; height: 94vh; overflow-y:scroll; overflow-x: hidden; border-right: 1px solid #dce3e8;">
                <node-menu @addNode="addNode" @getSaveParam="getSaveParam" ref="nodeMenu" :saveParam="saveParam" :epoch="epoch" @getPreParam="getPreParam"
                :paramName="paramName" :projectName="projectName"></node-menu>
            </div>
            <div id="efContainer" ref="efContainer" class="container" v-flowDrag>
                <template v-for="node in data.nodeList">
                    <flow-node
                        ref="flowNode"
                      :id="node.id"
                      :key="node.id"
                      :node="node"
                        class="nodes"
                      :activeElement="activeElement"
                      @clickNode="clickNode"
                    >
                    </flow-node>
                </template>
              <con ref="con" :message="message" :isShow="isShow" :chartIsShow="chartIsShow" :loss="loss"></con>
                <div style="position:absolute;top: 2000px;left: 2000px;">&nbsp;</div>
            </div>
            <div style="width: 300px;border-left: 1px solid #dce3e8;background-color: #FBFBFB; z-index: 100;">
                <flow-node-form ref="nodeForm" @openDataUpload="openDataUpload" @changePackageName="changePackageName"></flow-node-form>
            </div>
        </div>
      <drawer ref="drawer" :drawer="drawer" :dataUpload="dataUpload" :projectName="projectName" @closeDraw="closeDraw" :nodeList="data.nodeList"
              @closeDataDraw="closeDataDraw" @changeDataImgList="changeDataImgList" :dataImgList="dataImgList" :conn="conn"
              style="z-index: 101"></drawer>
    </div>

</template>

<script>

// import './jsplumb'
import {easyFlowMixin} from '@/components/mixins'
import flowNode from '../components/node'
import nodeMenu from '../components/node_menu'
import FlowNodeForm from '../components/node_form'
import lodash from 'lodash'
// import {jsPlumb} from "@/components/jsplumb";
import {getDataA, getParams} from "@/components/data_A";
import drawer from "@/components/drawer";
import navi from "@/components/nav"
import con from "@/components/console";
// import $ from 'jquery'
import Jsplumb from 'jsplumb';
const jsPlumb = Jsplumb.jsPlumb;
import Utils from './utils.js';

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
          isShow: false,
          message: "显示控制台信息",
          chartIsShow: false,
          saveParam: "",
          epoch: "100",
          downloadLoading:false,
          i: 0,
          packname: "",
          drawer: false,
          dataUpload: false,
          projectName: '未命名',
          paramName: 'best-model',
          createDate: "",
          dataImgList: [],
          conn: null,
          loss: {},
          flag: "0",
          savePre: "不使用预训练"
        }
      },
      // 一些基础配置移动该文件中
      mixins: [easyFlowMixin],
      components: {
        flowNode, nodeMenu, FlowNodeForm, drawer, navi, con
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
        console.log(this.$route.query.name)
        if(this.$route.query.name){
          this.projectName = this.$route.query.name
        }
        if(this.$route.query.flag){
          this.flag = this.$route.query.flag
        }
        this.createDate = this.$route.query.createdate
        // this.jsPlumb = jsPlumb.getInstance()
        // this.$nextTick(() => {
        //   // 默认加载流程A的数据、在这里可以根据具体的业务返回符合流程数据格式的数据即可
        this.dataReload()
        this.$refs.nodeMenu.getProjectName(this.projectName)
        // })
        window.onbeforeunload = () =>{
          return '请确认工程保存后离开'
        }
      },
      beforeRouteEnter(to, from, next) {
        console.log(' beforeRouteEnter !')
        next()
      },
      beforeRouteLeave(to, from , next) {
        this.$http.post("http://59.77.17.71:5001/visual/leave",{project: this.projectName})
        const answer = window.confirm('请确认工程保存后离开')
        answer ? next() : next(false)
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
            this.jsPlumb.reset();
            let that = this
            this.jsPlumb.importDefaults(this.jsplumbSetting)
            jsPlumb.bind('click', function (conn) {
              let r = confirm("确定删除连线吗？");
              if (r === true) {
                jsPlumb.deleteConnection(conn);
                that.conn = jsPlumb.getAllConnections()
              }
            });
            jsPlumb.bind("connection", function (conn) {
              console.log(conn)
              if (conn.sourceId === conn.targetId) {
                alert("不能连接本身节点！");
                jsPlumb.deleteConnection(conn.connection)
              }else {
                that.conn = jsPlumb.getAllConnections()
              }
            });
            // jsPlumb.bind('endpointClick', function (conn) {
            //   var data = getData(conn.element.innerText, conn.anchor.x, conn.anchor.y);
            //   that.$message(data);
            // })
            this.jsPlumb.setSuspendDrawing(false, true);
            console.log(this.$route.query.flag)
            if(this.$route.query.flag) {
              // this.$nextTick(()=>{
              //     console.log(this.$route.params.param)
              //     console.log(this.$route.params.nodeL)
              this.projectName = this.$route.query.name
              console.log(this.projectName)
              this.$http.post("http://59.77.17.71:5001/visual/getproject",{name: this.projectName}).then(res=>{
                console.log(res.data)
                let a = res.data.replaceAll("'", "\"").replaceAll("T","t").replaceAll("F","f")
                console.log(a)
                console.log(a[512])
                let data = JSON.parse(a)
                // let param = data["params"]
                this.data.nodeList = data["nodeList"]
                console.log(this.data.nodeList)
                let saveP = data["saveP"]
                console.log(saveP)
                this.paramName = saveP[2]
                this.epoch = saveP[1]
                let type = ["保存最优参数", "保存最后一轮参数", "保存指定轮数参数", "不保存参数",""]
                let f_type = ["best", "last", "given", "nope",""]
                let index = f_type.indexOf(saveP[0])
                this.saveParam = type[index]
                console.log(this.saveParam)
                this.$refs.nodeMenu.initselect(this.saveParam)
                // this.$refs.nodeMenu.initselect();
                console.log(this.data.nodeList)
                // })
                let lastNode = null
                this.$nextTick(()=>{
                  this.data.nodeList.forEach(node=>{
                    console.log(node)
                    this.setNodeStyle(lastNode, node)
                    lastNode = node
                  })
                  data["nodes"].forEach(node=>{
                    this.data.nodeList.push(node)
                    this.setNodeStyle(null, node)
                  })
                  this.conn = jsPlumb.getAllConnections()
                })
              })
            }
            if(this.flag === "0"){
              this.$refs.nav.saveProject("auto")
            }
            // 会使整个jsPlumb立即重绘。
            // this.$nextTick(() => {
            //   if(this.$route.params.param){
            //     console.log(this.$route.params.param)
            //     console.log(this.$route.params.nodeL)
            //     this.data.nodeList = this.$route.params.nodeL
            //     this.data.nodeList.forEach(node=> {
            //       this.setNodeStyle(node)
            //     })
            //   }
            //   this.jsPlumb.setSuspendDrawing(false, true);
            // })
            // this.$nextTick(()=>{
            //   if(this.$route.params.param) {
            //     let lastNode = null
            //     var common = {
            //       endpoint: 'Rectangle',
            //       connector: ['Bezier'],
            //       anchor: ['Left', 'Right']
            //     }
            //     this.data.nodeList.forEach(node => {
            //       if (lastNode != null) {
            //         console.log(node)
            //         console.log(lastNode)
            //         console.log(document.getElementById(node.id))

            //       }
            //       lastNode = node
            //     })
            //   }
            //   this.repaintEverything()
            // })
          })
        },
        /**
         * 拖拽结束后添加新的节点
         * @param evt
         * @param nodeMenu 被添加的节点对象
         * @param mousePosition 鼠标拖拽结束的坐标
         */
        addNode(evt, nodeMenu) {
          Utils.$emit("reload", "msg")
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
          console.log(nodeId);
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
          console.log(index);
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
          let params = getParams(node.name);
          for(let i = 0; i < params.length; i++){
            console.log(params[i])
            node[params[i].name] = params[i].init;
          }
          console.log(node);
          /**
           * 这里可以进行业务判断、是否能够添加该节点
           */
          this.data.nodeList.push(node)
          this.setNodeStyle(null, node)
        },
        setNodeStyle(lastNode, node){
          let nodeId = node.id
          let nodeName = node.name
          console.log(nodeId)
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
                    console.log(data.anchors[j])
                    jsPlumb.addEndpoint(nodeId, {
                      anchor: data.anchors[j],
                      uuid: nodeId + "top",
                      isSource: false,
                      isTarget: true,
                    },baseStyle)
                  }else{
                    jsPlumb.addEndpoint(nodeId, {
                      anchor: data.anchors[j],
                      // uuid: nodeId + data.names[j],
                      uuid: nodeId + "bottom",
                      isSource: true,
                      isTarget: false
                    },baseStyle)
                  }
                }
                break;
              }
            }
            this.jsPlumb.setSuspendDrawing(false, true);
            console.log(node)
            console.log(nodeId)
            console.log(document.getElementById(nodeId))
            this.$nextTick(()=>{
              jsPlumb.draggable(nodeId, {
                containment: 'parent',
                drag: function () {
                  jsPlumb.repaintEverything();
                }
              })
              if(lastNode != null) {
                  console.log(document.getElementById(node.id))
                  if(lastNode != null) {
                    jsPlumb.connect({
                      uuids: [lastNode.id + "bottom", node.id + "top"]
                    }, baseStyle)
                  }
                this.jsPlumb.repaintEverything();
              }
            })
            this.jsPlumb.setSuspendDrawing(false, true);
          })
        },
        clickNode(nodeId) {
          console.log(nodeId)
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
              console.log(this.jsPlumb)
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
              jsPlumb.removeAllEndpoints(nodeId);
            })
            console.log(nodeId)
            for(let i = 0; i < this.data.nodeList.length; i++){
              let node = this.data.nodeList[i]
              if(node.id === nodeId){
                this.data.nodeList.splice(i, 1)
              }
            }
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
            this.$refs.con.getLine();
          }
        },
        getSaveParam(saveParam, epoch, paramName){
          this.saveParam = saveParam;
          this.epoch = epoch;
          this.paramName = paramName;
        },
        openDataUpload(){
          this.dataUpload = true
        },
        changePackageName(packname){
          this.packname = packname
          console.log(this.packname)
        },
        closeDraw(){
          this.drawer = false;
        },
        closeDataDraw(){
          this.dataUpload = false;
        },
        openDrawer(){
          this.drawer = true;
          this.$refs.drawer.openTest()
        },
        changeDataImgList(dataImgList){
          this.dataImgList = dataImgList
        },
        getLoss(loss){
          this.loss = loss
          console.log(this.loss)
          console.log(this.loss["train_loss"])
          this.$refs.con.getLine(this.loss)
          if(this.loss["train_loss"].length > 0){
            this.chartIsShow = true
          }
        },
        resetLoss(){
          this.loss = {}
        },
        changeProjectName(name){
          this.projectName = name
        },
        uploadParams(){
          this.$refs.drawer.openParams()
        },
        getPreParam(savePre){
          this.savePre = savePre
          console.log(this.savePre)
        }
      },
    }
</script>
