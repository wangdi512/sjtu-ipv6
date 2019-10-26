<template>
  <el-menu
    :default-active="this.$route.path"
    class="el-menu-demo"
    mode="horizontal"
    background-color="#050e1e"
    text-color="#fff"
    active-text-color="#ffd04b"
  >
    <router-link to="/">
      <el-menu-item index="/">重新上传</el-menu-item>
    </router-link>
    <router-link to="/dashboard3">
      <el-menu-item index="/dashboard3">处理中心</el-menu-item>
    </router-link>
    <router-link to="/dashboard2">
      <el-menu-item index="/dashboard2">处理中心</el-menu-item>
    </router-link>
    <router-link to="/dashboard">
      <el-menu-item index="/dashboard">恶意域名</el-menu-item>
    </router-link>
  </el-menu>
</template>
<script>
</script>
<style lang="scss">
.el-menu--horizontal > a {
  float: right;
}

.el-menu.el-menu--horizontal {
  border-bottom: solid 1px #666e98;
}
</style>