<template>
  <el-tabs v-model="activeName" @tab-click="handleClick" class="tab">
    <el-tab-pane label="服务器连接设置" name="server">
      <p style="font-size: medium; font-weight: bold">服务器连接设置</p>
       <el-table
        :data="serverlist"
        stripe
        :row-style="{height:'60px'}"
        style="width: 100%; font-size: medium">
        <el-table-column
          prop="host"
          label="ip地址"
          min-width="300">
        </el-table-column>
        <el-table-column
          prop="port"
          label="端口号"
          min-width="300">
        </el-table-column>
        <el-table-column
          prop="user"
          label="用户名"
          min-width="300">
        </el-table-column>
         <el-table-column
          label="连接状态"
          min-width="300">
          <template slot-scope="scope">
            <el-button @click="connect(scope.row)" v-if="scope.row.state === 'none'">连接</el-button>
            <span v-if="scope.row.state === 'connect'" style="color: green">已连接</span>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane label="GPU与显存管理" name="gpu">
      <p style="font-size: medium; font-weight: bold">GPU与显存信息</p>
       <el-table
        :data="gpulist"
        stripe
        :row-style="{height:'60px'}"
        style="width: 100%; font-size: medium">
        <el-table-column
          prop="no"
          label="显卡编号"
          min-width="300">
        </el-table-column>
        <el-table-column
          prop="memory"
          label="显存占用"
          min-width="300">
        </el-table-column>
        <el-table-column
          prop="util"
          label="GPU利用率"
          min-width="300">
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane label="CPU与内存管理" name="cpu">
      <el-descriptions title="CPU管理" direction="vertical" :column="2" border>
        <el-descriptions-item label="CPU利用率" contentStyle="font-size: medium; width: 33%" labelStyle="font-size: medium">{{cpu}}</el-descriptions-item>
        <el-descriptions-item label="内存使用率" contentStyle="font-size: medium" labelStyle="font-size: medium">
          {{memory}}</el-descriptions-item>
      </el-descriptions>
      <el-descriptions title="内存管理" direction="vertical" :column="3" border style="margin-top: 5vh">
        <el-descriptions-item label="总计" contentStyle="font-size: medium; width: 33%" labelStyle="font-size: medium">{{memory_list[0]}}</el-descriptions-item>
        <el-descriptions-item label="已用" contentStyle="font-size: medium; width: 33%" labelStyle="font-size: medium">{{ memory_list[1] }}</el-descriptions-item>
        <el-descriptions-item label="空闲" contentStyle="font-size: medium; width: 33%" labelStyle="font-size: medium">{{ memory_list[2] }}</el-descriptions-item>
        <el-descriptions-item label="共享" contentStyle="font-size: medium; width: 33%" labelStyle="font-size: medium">{{ memory_list[3] }}</el-descriptions-item>
        <el-descriptions-item label="缓冲/缓存" contentStyle="font-size: medium; width: 33%" labelStyle="font-size: medium">{{ memory_list[4] }}</el-descriptions-item>
        <el-descriptions-item label="可用" contentStyle="font-size: medium; width: 33%" labelStyle="font-size: medium">{{ memory_list[5] }}</el-descriptions-item>
    </el-descriptions>
    </el-tab-pane>
  </el-tabs>
</template>
<script>
  export default {
    data() {
      return {
        activeName: 'server',
        cpu: '',
        memory: '',
        memory_list: [],
        gpulist: [],
        serverlist: [{'host': "59.77.17.71", 'port': '22', 'user': 'DL', 'state': 'connect'},
          {'host': "10.26.34.14", 'port': '22', 'user': 'imt-a4000', 'state': 'none'}]
      };
    },
    // mounted(){
    //   let that = this
    //
    //   setInterval(
    //     function (){
    //       that.$http.get("http://59.77.17.71:5001/getcpuinfo").then(res=>{
    //         that.cpu = res.data["cpu_state"]
    //         that.memory = res.data["memory_state"]
    //         that.memory_list = res.data["memory"]
    //       })
    //       that.$http.get("http://59.77.17.71:5001/getgpuinfo").then(res=>{
    //         that.gpulist = res.data["gpu_info"]
    //       })
    //     }, 1000
    //   )
    // },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      },
      connect(serve){
        let that = this
        this.$prompt('请输入密码', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({ value }) => {
          that.$http.post("http://59.77.17.71:5001/connectserver", {"host": serve.host, "port": serve.port, "user": serve.user, "password": value}).then(res=>{
            if(res.state === "success"){
              alert("连接成功！")
            }else{
              alert("连接失败")
            }
          })
        })
      }
    }
  };
</script>
<style>
.tab{
  width: 80%;
  margin-left: 10%;
  margin-top: 5vh;
}
</style>