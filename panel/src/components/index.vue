<template>
    <div>
    <div class="title">深度学习系统</div>
    <div class="card" id="card1" @click="tocode"  @mouseenter="changeImageSrc(1, 'hover')"
         @mouseleave="changeImageSrc(1, '')">
        <img :src="codeimg" class="img" id="img1"/>
        <div class="text" id="text1">代码开发</div>
    </div>
    <div class="card" id="card2" @click="tovision" @mouseenter="changeImageSrc(2, 'hover')"
         @mouseleave="changeImageSrc(2, '')">
        <img :src="visionimg" class="img" id="img2" alt=""/>
        <div class="text" id="text2">可视化开发</div>
    </div>
    <div class="card" id="card3" @click="toapplication" @mouseenter="changeImageSrc(3, 'hover')"
         @mouseleave="changeImageSrc(3, '')">
        <img :src="applicationimg" class="img" id="img3" alt=""/>
        <div class="text" id="text3">应用</div>
    </div>
  </div>
</template>
<script>
export default {
  name: "index",
  data() {
    return {
      codeimg: require("@/assets/code.svg"),
      visionimg: require("@/assets/drag.svg"),
      applicationimg: require("@/assets/application.svg")
    }
  },
  methods: {
    tocode() {
      this.$http.post("http://59.77.17.71:5001/code/findname").then(res=>{
        console.log(res)
        var d = new Date();
        let createDate = d.getFullYear()+ "-" + (d.getMonth()+1) + "-" + d.getDate()
        this.$router.replace({name: 'code', query: {name: res.data, createdate: createDate}})
      })
    },
    tovision() {
      this.$http.post("http://59.77.17.71:5001/visual/findname").then(res=>{
        console.log(res)
        var d = new Date();
        let createDate = d.getFullYear()+ "-" + (d.getMonth()+1) + "-" + d.getDate()
        console.log(createDate)
        this.$router.replace({name: 'panel', query: {name: res.data, createdate: createDate}})
      })
    },
    toapplication() {
      this.$router.replace({name: 'test'})
    },
    changeImageSrc(key, way) {
      let tempStr = way === 'hover' ? '_hover' : ''
      switch (key) {
        case 1:
          this.codeimg = require(`@/assets/code${tempStr}.svg`)
          break
        case 2:
          this.visionimg = require(`@/assets/drag${tempStr}.svg`)
          break
        case 3:
          this.applicationimg = require(`@/assets/application${tempStr}.svg`)
          break
      }
    }
  }
}
</script>

<style scoped>
  .card{
      height: 50vh;
      width: 25vw;
      margin-left: 5vw;
      margin-top: 10vh;
      float: left;
      border: 5px solid #2417ff;
      box-shadow: 3px 3px 30px #909090;
      transition: border 0.5s;
      /* 兼容旧版Firefox */
      -moz-transition: border 0.5s;
      /* 兼容旧版Safari and Chrome */
      -webkit-transition: border 0.5s;
  }
  .card :hover{
      border: #409EFA;
  }
  .img{
      height: 40vh;
      width: 100%;
      display: block;
  }
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
  .text{
      text-align: center;
      align-content: center;
      line-height: 10vh;
      background-color: white;
      width: 100%;
      height: 10vh;
      color: black;
      font-size: large;
      transition: background-color 1s, color 0.5s, font-size 0.5s;
      /* 兼容旧版Firefox */
      -moz-transition: background-color 1s, color 0.5s, font-size 0.5s;
      /* 兼容旧版Safari and Chrome */
      -webkit-transition: background-color 1s, color 0.5s, font-size 0.5s;
  }
  .card :hover+.text{
      background-color: #334BFC;
      color: white;
      font-size: x-large;
  }
</style>