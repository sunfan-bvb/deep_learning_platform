<template>
  <div>
    <div style="position: fixed; bottom: 0px; height: 30%; width: 100%; z-index: 101;" v-show="isShow">
      <el-tabs v-model="activeName" type="border-card" style="height: 100%; width: 100%">
      <el-tab-pane label="控制台" name="console">{{message}}</el-tab-pane>
    </el-tabs>
    </div>
    <div style="position: fixed; bottom: 0px; height: 50%; width: 100%; z-index: 101;" v-show="chartIsShow">
      <el-tabs v-model="activeNameC" type="border-card" style="height: 100%; width: 100%">
        <el-tab-pane label="图表" name="chart" id="chart" style="height: 100%; width: 100%;">
          <div style="display: inline-block;" v-show="!empty">
            <div class="chart" ref="line" id="line1" style="height:350px; width: 500px; float: left"></div>
            <div style="background-color: #565758; height: 300px; width: 1px; float: left; margin: 15px 15px 15px 15px;"></div>
            <div class="chart" ref="line" id="line2" style="height:350px; width: 500px; float: left"></div>
          </div>
          <div style="width: calc(100% - 200px)">
            <el-empty :image-size="160" v-show="empty"></el-empty>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>

export default {
  name: "con",
  data(){
    return{
      activeName: "console",
      activeNameC: "chart",
      myChart1: null,
      myChart2: null,
      empty: true
    }
  },
  props:["message", "isShow", "chartIsShow", "loss"],
  methods:{
    getLine(loss) {
      console.log(loss)
      if(loss["train_loss"].length > 0){
        this.empty = false
      }
      console.log("getLine")
      const echarts = require('echarts');
      require('echarts-gl');
      this.myChart1 = echarts.init(document.getElementById("line1"), 'light');
      this.myChart2 = echarts.init(document.getElementById("line2"), 'light');
      // 指定图表的配置项和数据
      // option将要设置以下字段感觉就足够使用了
      let epochs = []
      for(let i = 0; i < loss["train_loss"].length; i++){
        epochs.push(i+1)
      }
      console.log(epochs)
      let option= {
        legend: {
            data: ['训练集'+loss['matrix'], '验证集'+loss['matrix']]
        },
        xAxis: {
          type: 'category',   // 还有其他的type，可以去官网喵两眼哦
          data: epochs,   // x轴数据
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
              name: '训练集'+loss['matrix'],
              data: loss["train_matrix"],
              type: 'line'
            },
            {
              name: '验证集'+loss['matrix'],
              data: loss["val_matrix"],
              type: 'line'
            }
        ]
      }
      let loss_option= {
        legend: {
            data: ['训练集loss','验证集loss']
        },
        xAxis: {
          type: 'category',   // 还有其他的type，可以去官网喵两眼哦
          data: epochs,   // x轴数据
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
              data: loss["train_loss"],
              type: 'line'
            },
            {
              name: '验证集loss',
              data: loss["val_loss"],
              type: 'line'
            }
        ]
      }
      this.myChart1.setOption(option);
      this.myChart1.resize();
      this.myChart2.setOption(loss_option);
      this.myChart2.resize();
    },
  }
}
</script>

<style scoped>

</style>