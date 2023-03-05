<template>
  <div>
    <el-row style="height: 6vh;">
      <!--顶部工具菜单-->
      <el-col :span="24">
          <div class="ef-tooltar">
            <el-button type="text" @click="changeName" style="font-size: larger; margin-right: 1vw; color: black">{{projectName}}</el-button>
<!--            <el-button type="primary" icon="el-icon-s-home" @click="toIndex">工程面板</el-button>-->
            <el-divider direction="vertical"></el-divider>
            <el-button @click="consoleClick">控制台</el-button>
            <el-divider direction="vertical"></el-divider>
<!--            <el-button @click="chartClick">图表</el-button>-->
<!--              <el-divider direction="vertical"></el-divider>-->
            <el-button type="success" icon="el-icon-caret-right" plain @click="runCode">运行</el-button>
            <el-divider direction="vertical"></el-divider>
            <el-button type="success" icon="el-icon-cpu" plain @click="debugCode">调试</el-button>
            <el-button type="primary" @click="saveProject">保存</el-button>
          </div>
      </el-col>
  </el-row>
  <Editor style="z-index: 1; width: 100%; height: 92vh;" @getCode="getCode" ref="Editor" :code="code" @onchange="onedit"/>
  <div style="position: fixed; bottom: 0px; height: 30%; width: 100%; left: 40px; z-index: 100" v-show="isShow">
    <el-tabs v-model="activeName" type="border-card" style="height: 100%; width: 100%">
    <el-tab-pane label="控制台" name="console">
      <div v-show="loadIsShow" style="width: 100%; height: 100%; text-align: center; justify-content: center;">
        <div style="font-size: 5vh; color: dodgerblue"><i class="el-icon-loading"></i></div>
        <div>运行中···</div>
      </div>
      <div v-show="!loadIsShow">{{message}}</div>
    </el-tab-pane>
  </el-tabs>
  </div>
  </div>
</template>

<script>
import Editor from './Editor'
import {save_log} from "@/components/utils.js";

export default {
  name: "code",
  data() {
    return{
      projectName: "未命名",
      isShow: false,
      activeName: "console",
      activeNameC: "chart",
      activeNameP: "params",
      activeNameT: "paramsInfo",
      consoleType: "",
      message: "显示控制台信息",
      chartIsShow: false,
      tableData: [{'name': 'version', 'value': '1.3.1'},
        {'name': 'array', 'value': [[1, 2, 3, 4 ,5, 6, 7], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4 ,5, 6, 7],
            [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4 ,5, 6, 7], [1, 2, 3, 4, 5, 6, 7]]}],
      code: "",
      value: "",
      tablevalue: [],
      colvalue: [],
      valueIsShow: false,
      tableIsShow: false,
      paramsIsShow: false,
      loadIsShow: false,
      flag: false,
      createDate: "",
      change: false
    }
  },
  components: {
    Editor
  },
  created: function (){
    this.createDate = this.$route.query.createdate
    let data = this.tableData;
      for(var i = 0; i < data.length; i++){
        if(Array.isArray(data[i].value)){
          let a = data[i].value;
          var shape = a.length.toString();
          a = a[0];
          while(Array.isArray(a)){
            shape += ("*" + a.length.toString());
            a = a[0];
          }
          data[i]["showValue"] = shape + " Array";
        }else{
          data[i]["showValue"] = data[i].value;
        }
      }
      console.log(data);
      this.tableData = data;
      this.projectName = this.$route.query.name
      if(this.$route.query.code) {
        this.code = this.$route.query.code
        console.log(this.code)
      }
  },
  mounted() {
    window.onbeforeunload = () =>{
      return '请确认工程保存后离开'
    }
  },
  beforeRouteEnter(to, from, next) {
    console.log(' beforeRouteEnter !')
    next()
  },
  beforeRouteLeave(to, from , next) {
    const answer = window.confirm('请确认工程保存后离开')
    answer ? next() : next(false)
  },
  methods: {
    toIndex(){
      this.$router.push('/projects');
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
    clickData(row){
      this.paramsIsShow = true;
      this.isShow = false;
      this.chartIsShow = false;
      let value = row.value;
      if(Array.isArray(value) === false){
        this.valueIsShow = true;
        this.tableIsShow = false;
        this.value = value;
      }else{
        this.valueIsShow = false;
        this.tableIsShow = true;
        let list = [];
        let col = [];
        for(var k = 0; k < value[0].length; k++){
          col.push((k+1).toString());
        }
        for(var i = 0; i < value.length; i++){
          let dict = {};
          for(var j = 0; j< value[i].length; j++){
            dict[j+1] = value[i][j];
          }
          list.push(dict);
        }
        console.log(list);
        console.log(col);
        this.tablevalue = list;
        this.colvalue = col;
      }
    },
    getCode(code){
      this.code = code
    },
    requestMessage(){
      this.$http.get("http://59.77.17.71:5001/code/errormessage").then(res=> {
        console.log(res)
      })
    },
    runCode(){
      this.loadIsShow = true;
      this.isShow = true;
      var a = this.code.split("\n");
      var f_code = "";
      a.forEach(function(item){
        f_code = f_code + item + "<br>";
      });
      let t = window.setInterval(this.requestMessage, 1000);
      console.log(f_code)
      this.$http.post("http://59.77.17.71:5001/code/run",{code:f_code}).then(res=>{
        console.log(res)
        let ds = res.data.d.split("++++");
        let df = "";
        ds.forEach(function (d) {
          df = df + d.slice(2, -1);
        });
        this.message = df.replaceAll("\\n", "\n");
        this.loadIsShow = false;
        console.log(this.message)
        save_log("运行代码："+ this.projectName + ", 输出结果：" + this.message.replaceAll("\n", ""))
        window.clearInterval(t);
      });

    },
    removeTab(tagname){
      console.log(tagname)
      this.paramsIsShow = false;
    },
    debugCode(){
      this.$prompt('请输入开始调试行数', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /^\d+$/,
          inputErrorMessage: '格式不正确，请输入整数'
        }).then(({ value }) => {
          var a = this.code.split("\n");
          if(value > a.length){
            this.$message.error("超过代码行数！")
          }else {
            a.splice(value - 1, 0, "import wdb", "wdb.set_trace()");
            var f_code = "";
            a.forEach(function(item){
              f_code = f_code + item + "<br>";
            });
            this.$http.post("http://59.77.17.71:5001/debug",{code:f_code, project: this.projectName})
          }
        })
    },
    changeName(){
      this.$prompt('输入工程名', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({ value }) => {
        this.$http.post("http://59.77.17.71:5001/code/changename", {name: value, oldname: this.projectName}).then(res => {
          if (res.data === "success") {
            save_log("修改工程名，由"+ this.projectName + "改为" + value)
            this.projectName = value;
          } else if (res.data === "exist") {
            this.$message.error("不能和现有工程名相同！")
          } else {
            this.$message.error("新建项目请先保存再重命名！")
          }
        })
      })
    },
    saveProject(){
      this.$http.post("http://59.77.17.71:5001/code/save", {code: this.code, name:this.projectName, date: this.createDate}).then(res=>{
        if(res.data === "success"){
          this.$message({message:"保存成功！",type:'success'})
          this.change = false
          save_log("IDE工程保存：" + this.projectName)
        }
      })
    },
    onedit(){
      this.change = true
    }
  }
}
</script>

<style scoped>
</style>