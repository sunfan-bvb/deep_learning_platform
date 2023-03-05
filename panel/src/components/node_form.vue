<template>
    <div>
        <div class="ef-node-form">
            <div class="ef-node-form-header">
                设置
            </div>
            <div class="ef-node-form-body">
                <el-form :model="node" ref="dataForm" label-width="100px" v-show="type === 'node'">
                  <div v-for="p in params" :key="p.index">
                    <el-form-item :label="p.param">
                    <el-input v-show="p.type==='input'" v-model="node[p.name]" type="text"></el-input>
                      <el-slider v-model="node[p.name]" v-show="p.type === 'slide'"></el-slider>
                    <el-select v-show="p.type==='select'" placeholder="请选择" v-model="node[p.name]">
                      <el-option
                              v-show="p.name!=='package'"
                              v-for="item in p.select"
                              :key="item"
                              :label="item"
                              :value="item">
                      </el-option>
                      <el-option
                              v-show="p.name==='package'"
                              v-for="item in packages"
                              :key="item"
                              :label="item"
                              :value="item">
                      </el-option>
                    </el-select>
                      <el-button v-show="p.type==='upload'" @click="openUpload">上传数据集</el-button>
                  </el-form-item>
                  </div>
                    <el-form-item v-show="init">
                        <el-button icon="el-icon-close" @click="reset">重置</el-button>
                        <el-button type="primary" icon="el-icon-check" @click="save">保存</el-button>
                    </el-form-item>
                </el-form>

                <el-form :model="line" ref="dataForm" label-width="80px" v-show="type === 'line'">
                    <el-form-item label="条件">
                        <el-input v-model="line.label"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button icon="el-icon-close">重置</el-button>
                        <el-button type="primary" icon="el-icon-check" @click="saveLine">保存</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>

</template>

<script>
    import { cloneDeep } from 'lodash'
    import { getNodeParams,getParams} from "@/components/data_A";
    import utils from "@/components/utils";

    export default {
        data() {
            return {
                visible: true,
                // node 或 line
                type: 'node',
                node: {},
                line: {},
                data: {},
                params: {},
                init: false,
                optimizerList: [{
                    key: 'adam',
                    name: 'adam'
                }, {
                    key: 'sgd',
                    name: 'sgd'
                }, {
                    key: 'momentum',
                    name: 'momentum'
                }],
                fileList:[],
                imgList: [],
                drawer: false,
                packages:[]
            }
        },
        mounted() {
          this.$http.get(
              "http://59.77.17.71:5001/visual/getpackage",
          ).then(res => {
            console.log(res)
            let p = res.data.split(" ")
            p.shift()
            this.packages = p
          })
        },
      methods: {
            /**
             * 表单修改，这里可以根据传入的ID进行业务信息获取
             * @param data
             * @param id
             */
            nodeInit(data, id) {
                this.type = 'node'
                this.data = data
                console.log(data)
                data.nodeList.filter((node) => {
                    if (node.id === id) {
                        this.node = cloneDeep(node)
                        this.params = getParams(node.name)
                        for(var i = 0; i < this.params.length; i++){
                          console.log(this.params[i].name)
                          this.node[this.params[i].name]=null;
                        }
                        console.log(this.node)
                        // this.node.params = getNodeParams(node.name)
                        this.init = true
                    }
                })
            },
            nodeClick(data, id){
              this.type = 'node'
                this.data = data
                console.log(data)
                data.nodeList.filter((node) => {
                    if (node.id === id) {
                        this.node = cloneDeep(node)
                        this.params = getParams(node.name)
                        // let params = getNodeParams(node.name);
                        // for(var i = 0; i < params.length; i++){
                        //   console.log(node[params[i]])
                        //   console.log(this.node[params[i]])
                        //   this.node[params[i]] = node[params[i]];
                        // }
                        // console.log(this.node)
                        // console.log(this.params)
                        this.init = true
                    }
                })
            },
            lineInit(line) {
                this.type = 'line'
                this.line = line
            },
            // 修改连线
            saveLine() {
                this.$emit('setLineLabel', this.line.from, this.line.to, this.line.label)
            },
            save() {
                this.data.nodeList.filter((node) => {
                    if (node.id === this.node.id) {
                        node.name = this.node.name
                        let params = getNodeParams(node.name);
                        for(var i = 0; i < params.length; i++){
                          console.log(this.node[params[i]])
                          console.log(node[params[i]])
                          node[params[i]] = this.node[params[i]];
                        }
                        this.$message.success('保存成功');
                        console.log(node);
                        console.log(this.data.nodeList)
                        this.$emit('repaintEverything')
                        this.$emit('rewriteNodeList', this.data.nodeList)
                    }
                    if(node.type === "upload"){
                      this.$emit('changePackageName', node.packname)
                    }
                })
              this.$nextTick(()=>{
                utils.$emit('saveProject');
              })
            },
          reset(){
              this.data.nodeList.filter((node) => {
                    if (node.id === this.node.id) {
                        node.name = this.node.name
                        let params = getParams(node.name);
                        for(var i = 0; i < params.length; i++){
                          node[params[i].name] = params[i].init;
                        }
                        this.$emit('repaintEverything')
                    }
              })
              this.data.nodeList.filter((node) => {
                    if (node.id === this.node.id) {
                        this.node = cloneDeep(node)
                        this.params = getParams(node.name)
                        console.log(this.node)
                        this.init = true
                    }
                })
            this.$nextTick(()=>{
                utils.$emit('saveProject');
              })
          },
          handleRemove(file, fileList) {
            console.log(file);
            console.log(fileList);
            console.log(this.imgList)
            this.fileList = fileList
            let i = 0
            this.imgList.forEach(f =>{
              if(f.name === file.name){
                this.imgList.splice(i, 1)
              }
              i ++;
            })
          },
          handlePreview(file) {
            console.log(file);
          },
          beforeRemove(file, fileList){
            console.log(fileList)
              return this.$confirm(`确定移除 ${ file.name }？`);
          },
          showSuccess(res, file){
            console.log(res)
            console.log(file)
            this.imgList.push(file[this.imgList.length])
            this.fileList.push({"name":res.name, "url": res.url})
            console.log(this.imgList)
            console.log(this.fileList)
          },
          openUpload(){
              for(let i = 0; i < (this.data.nodeList.length); i++){
                if(this.data.nodeList[i].name === "本地上传"){
                  console.log(this.data.nodeList[i])
                  if("packname" in this.data.nodeList[i] && this.data.nodeList[i].packname!== "" && this.data.nodeList[i].packname!== "undefined"){
                    this.$emit("openDataUpload")
                    utils.$emit('setname', this.data.nodeList[i]['packname']);
                  }else{
                    this.$message("请先填写数据包名并保存！")
                  }
                  break
                }
              }
          }
        }
    }
</script>

<style>
    .el-node-form-tag {
        position: absolute;
        top: 50%;
        margin-left: -15px;
        height: 40px;
        width: 15px;
        background-color: #fbfbfb;
        border: 1px solid rgb(220, 227, 232);
        border-right: none;
        z-index: 0;
    }
</style>
