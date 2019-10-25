<template>
  <div>
    <bg />
    <particles />
    <main>
      <div class="content">
        <header>基于ipv6的网络流量分析系统</header>
        <p>写简介写简介写简介写简介写简介写简介写简介写简介写简介写简介写简介</p>
        <el-upload
          class="upload-demo"
          action="https://jsonplaceholder.typicode.com/posts/"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :before-remove="beforeRemove"
          multiple
          :limit="3"
          :on-exceed="handleExceed"
          :file-list="fileList"
        >
          <el-button size="small" type="primary">点击上传</el-button>
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
export default {
  components: {
    bg,
    particles,
    foot
  }
};
</script>
<style lang="scss" scoped>
main {
  height: 90vh;
  display: flex;
  align-items: center;
  color: #ffffff;
  .content {
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
    }
    .el-button {
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