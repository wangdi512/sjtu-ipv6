<template>
  <el-menu
    :default-active="this.$route.path"
    class="el-menu-demo"
    mode="horizontal"
    background-color="#050e1e"
    text-color="#fff"
    active-text-color="#ffd04b"
  >
    <el-menu-item index="/dashboard3">
      <router-link to="/dashboard3">处理中心</router-link>
    </el-menu-item>

    <el-menu-item index="/dashboard2">
      <router-link to="/dashboard2">处理中心</router-link>
    </el-menu-item>

    <el-menu-item index="/dashboard">
      <router-link to="/dashboard">恶意域名</router-link>
    </el-menu-item>
  </el-menu>
</template>
<script>

</script>
<style lang="scss">
.el-menu--horizontal > .el-menu-item {
  float: right;
}

.el-menu.el-menu--horizontal {
  border-bottom: solid 1px #666e98;
}
</style>