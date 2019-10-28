<template>
  <el-menu
    :default-active="this.$route.path"
    class="el-menu-demo"
    mode="horizontal"
    background-color="#050e1e"
    text-color="#fff"
    active-text-color="#ffd04b"
  >
    <router-link to="/" class="left">
      <el-menu-item index="/"><i class="el-icon-back"></i>重新上传</el-menu-item>
    </router-link>
    <router-link to="/dashboard3">
      <el-menu-item index="/dashboard3">物联网</el-menu-item>
    </router-link>
    <router-link to="/dashboard2">
      <el-menu-item index="/dashboard2">恶意域名</el-menu-item>
    </router-link>
    <router-link to="/dashboard">
      <el-menu-item index="/dashboard">基础统计</el-menu-item>
    </router-link>
  </el-menu>
</template>
<script>
</script>
<style lang="scss">
.el-menu--horizontal > a {
  float: right;
  font-size:16px;
}
.left{
  float:left !important;
}
.el-menu.el-menu--horizontal {
  border-bottom: solid 1px #666e98;
}
.el-icon-back{
  color:white !important;
  font-size: 1.4em !important;
  font-weight: bolder !important;
}
</style>