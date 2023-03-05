<template>
    <div class="flow-menu" ref="tool">
        <el-input v-model="input" placeholder="请输入内容" style="width: 10vw; margin-top: 1vh"></el-input>
        <el-button type="primary" icon="el-icon-search" style="margin-left: 1vh" @click="search"></el-button>
        <div v-for="menu  in  menuList" :key="menu.id">
            <span class="ef-node-pmenu" @click="menu.open = !menu.open"><i :class="{'el-icon-caret-bottom': menu.open,'el-icon-caret-right': !menu.open}"></i>&nbsp;{{menu.name}}</span>
             <div v-show="menu.type === 'output' && menu.open">
                  <el-select placeholder="是否保存参数" v-model="saveParam" @change="onselect">
                    <el-option
                            v-for="item in saveList"
                            :key="item.key"
                            :label="item.name"
                            :value="item.name">
                    </el-option>
                  </el-select>
                  <div v-show="epochShow">
                    <el-tag>epoch: {{epoch}}</el-tag>
                    <el-button type="text" @click="editEpoch" style="padding-left: 5px">编辑训练轮数</el-button>
                  </div>
                  <div v-show="nameShow">
                    <el-tag>参数名: {{paramName}}</el-tag>
                    <el-button type="text" @click="editName" style="padding-left: 5px">编辑参数名</el-button>
                  </div>
             </div>
            <div v-show="menu.type === 'pre' && menu.open">
              <el-select placeholder="预训练参数选择" v-model="preparam" @change="onpreselect">
                <el-option
                        v-for="item in paramList"
                        :key="item.label"
                        :label="item.label"
                        :value="item.label">
                </el-option>
                <el-dropdown-item disabled v-show="paramList.length === 1">无已有预训练参数</el-dropdown-item>
              </el-select>
            </div>
            <div v-show="menu.type !== 'output' && menu.type !== 'pre'">
            <ul v-show="menu.open" v-for="child in menu.children" :key="child.id" class="ef-node-menu-ul">
              <span class="ef-node-pmenu" @click="child.open = !child.open"><i :class="{'el-icon-caret-bottom': child.open,'el-icon-caret-right': !child.open}"></i>&nbsp;{{child.name}}</span>
                <ul v-show="child.open" class="ef-node-menu-ul">
                <draggable @end="end" @start="move" v-model="child.children" :options="draggableOptions">
                    <li v-for="subMenu in child.children" class="ef-node-menu-li" :key="subMenu.id" :type="subMenu.type">
                        <i :class="subMenu.ico"></i> {{subMenu.name}}
                    </li>
                </draggable>
              </ul>
            </ul>
            </div>
        </div>
    </div>
</template>
<script>
    import draggable from 'vuedraggable'
    import {getMenu} from "@/components/data_A";

    var mousePosition = {
        left: -1,
        top: -1
    }

    export default {
        data() {
            return {
                activeNames: '1',
                // draggable配置参数参考 https://www.cnblogs.com/weixin186/p/10108679.html
                draggableOptions: {
                    preventOnFilter: false,
                    sort: false,
                    disabled: false,
                    ghostClass: 'tt',
                    // 不使用H5原生的配置
                    forceFallback: true,
                    // 拖拽的时候样式
                    // fallbackClass: 'flow-node-draggable'
                },
                // 默认打开的左侧菜单的id
                defaultOpeneds: ['1', '2', '3', '4'],
                menuList: [],
                saveList: [{
                      key: 'best',
                      name: '保存最优参数'
                  }, {
                      key: 'last',
                      name: '保存最后一轮参数'
                  }],
                // saveParam:"",
                // epoch: "100",
                epochShow: false,
                nodeMenu: {},
                // paramName: "best-model",
                nameShow: false,
                input: '',
                paramList:[],
                preparam: '不使用预训练'
            }
        },
        props:["epoch", "paramName", "saveParam", "projectName", "savePre"],
        components: {
            draggable
        },
        created() {
            /**
             * 以下是为了解决在火狐浏览器上推拽时弹出tab页到搜索问题
             * @param event
             */
            if (this.isFirefox()) {
                document.body.ondrop = function (event) {
                    // 解决火狐浏览器无法获取鼠标拖拽结束的坐标问题
                    mousePosition.left = event.layerX
                    mousePosition.top = event.clientY - 50
                    event.preventDefault();
                    event.stopPropagation();
                }
            }
            this.menuList = getMenu();
            console.log(this.menuList)
        },
      methods: {
            // 根据类型获取左侧菜单对象
            getProjectName(projectName){
                console.log(projectName)
                this.$http.post("http://59.77.17.71:5001/visual/gettestparam",{project: projectName}).then(res=>{
                  console.log(res)
                  let params = [{label: "不使用预训练"}]
                  res.data.params.forEach(data =>{
                    if(JSON.stringify(params).indexOf(JSON.stringify(data)) === -1){
                      params.push({label: data})
                    }
                  })
                  this.paramList = params
                }).catch(
                    this.paramList = [{label: "不使用预训练"}]
                )
            },
            getMenuByType(type) {
                for (let i = 0; i < this.menuList.length; i++) {
                    let children = this.menuList[i].children;
                    for (let j = 0; j < children.length; j++) {
                      let subChildren = children[j].children;
                      for(let k = 0; k < subChildren.length; k++){
                        if (subChildren[k].type === type) {
                            return subChildren[k]
                        }
                      }
                    }
                }
            },
            // 拖拽开始时触发
            move(evt) {
                var type = evt.item.attributes.type.nodeValue;
                this.nodeMenu = this.getMenuByType(type)
            },
            // 拖拽结束时触发
            end(evt) {
                this.$emit('addNode', evt, this.nodeMenu, mousePosition)
            },
            // 是否是火狐浏览器
            isFirefox() {
                var userAgent = navigator.userAgent
                return userAgent.indexOf("Firefox") > -1;
            },
            editEpoch(){
                this.$prompt('请输入训练轮数（epoch值）', '提示', {
                  confirmButtonText: '确定',
                  cancelButtonText: '取消',
                  inputPattern: /^\d+$/,
                  inputErrorMessage: '格式不正确，请输入整数'
                }).then(({ value }) => {
                    this.epoch = value;
                    this.$emit('getSaveParam', this.saveParam, this.epoch, this.paramName)
                })
            },
            onselect(){
              this.epochShow = this.saveParam === "保存指定轮数参数";
              this.nameShow = this.saveParam !== "不保存参数";
              console.log(this.saveParam)
              this.$emit('getSaveParam', this.saveParam, this.epoch, this.paramName)
            },
            onpreselect(){
              console.log(this.preparam)
              this.$emit('getPreParam', this.preparam)
            },
            editName(){
              this.$prompt('请输入参数名', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
              }).then(({ value }) => {
                  this.paramName = value;
                  this.$emit('getSaveParam', this.saveParam, this.epoch, this.paramName)
              })
            },
            initselect(saveParam){
              this.epochShow = saveParam === "保存指定轮数参数";
              this.nameShow = saveParam !== "不保存参数" && saveParam !== "";
              this.saveParam = saveParam
              console.log(saveParam)
              console.log(this.epochShow)
              console.log(this.nameShow)
            },
            search(){
              this.menuList.forEach(menu=>{
                menu.open = false
                menu.children.forEach(children=>{
                  children.open = false
                  children.children.forEach(child=>{
                    if(child.name.indexOf(this.input)>=0){
                      children.open = true
                      menu.open = true
                    }
                  })
                })
              })
            }
        }
    }
</script>
