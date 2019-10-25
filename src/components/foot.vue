<template>
  <div class="footer-link">
    <p>Copyright © 2019 上海交通大学</p>
    <p>
        联系我们: &nbsp;laijingzhi@sjtu.edu.cn
    </p>
  </div>
</template>

<script>
export default {
  name: "foot"
};
</script>

<style lang="scss">
.footer-link {
  position: relative;
  font-size: 18px;
  bottom: 0;
  left: 0;
  color: white;
  text-align: center;
  width: 100%;
  z-index: 1001;
  p {
    a {
      color: #e6e6fa;
      cursor: pointer;
    }
  }
}
</style>
