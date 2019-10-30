<template>
  <div>
    <bg />
    <particles />
    <main>
      <div class="content">
        <header>基于ipv6的网络流量分析系统</header>
        <p>一款集安全分析与数据可视化为一体的工具</p>
        <el-upload
          action="/test"
          :on-success="showResult"
          multiple
          :limit="1"
        >
          <el-button  type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传pcap文件</div>
        </el-upload>
      </div>
    </main>
    <foot></foot>
  </div>
</template>
<script>
import bg from "@/components/bg.vue";
import particles from "@/components/particles.vue";
import foot from "@/components/foot.vue";
import { mapMutations } from 'vuex'
export default {
  components: {
    bg,
    particles,
    foot
  },
  methods: {
     ...mapMutations([
      'initData' 
    ]),
    showResult(res){
      console.log(res.data);
      this.initData(res.data)
      this.$router.push("/dashboard4")
    }
  },
};
</script>
<style lang="scss" scoped>
main {
  height: 90vh;
  display: flex;
  align-items: center;
  color: #ffffff;
  .content {
    height:35%;
    z-index: 2;
    width: 50%;
    padding-right: 20px;
    margin-left: auto;
    padding-bottom: 20px;
    header {
      margin-bottom: 2rem !important;
      font-weight: bold;
      font-size: 3rem;
    }
    p {
      margin-bottom: 1em;
      font-size: 20px;
      line-height: 1.3;
    }
    .el-button {
      font-size: 20px;
      padding: 12px 20px !important;
      border-radius: 10px;
      margin-bottom: 0.5em;
      background-color: #006699;
    }
    .el-upload__tip{
        font-size: 14px;
        color: #ffffff;
    }
  }
}
</style>