<template>
  <div class="dashboard">
    <v-nav></v-nav>
    <main>
      <div class="item one">
        <column
          title="IPv6各服务提供商上下行流量大小"
          xName="服务商"
          yName="流量大小/Byte"
          :xData="['教育网','电信', '联通','移动','阿里','腾讯','亚马逊']"
          :label="[ '上行流量','下行流量' ]"
          :yData="this.chart5Ydata"
        ></column>
        <a href="#/dashboard">more&nbsp;>></a>
      </div>
      <div class="item two">
        <v-map></v-map>
          <a href="#/dashboard3">more&nbsp;>></a>
      </div>
      <div class="item three">
        <v-line
          title="一周内检测域名数变化"
          :xData="this.dateXdata"
          :yData="this.dateYdata"
          yName="数量/百条"
          xName="时间"
          :label="['检测域名数','检出恶意域名数']"
        ></v-line>
        <a href="#/dashboard2">more&nbsp;>></a>
      </div>
      <div class="item four">
        <h1>系统运行情况：</h1>
        <p>本日实时总流量大小为<strong>&nbsp;356143850&nbsp;</strong>Bytes</p>
        <p>本日ipv4流量大小为<strong>&nbsp;35330014&nbsp;</strong>Bytes</p>
        <p>本日ipv6流量大小为<strong>&nbsp;2842836&nbsp;</strong>Bytes</p>
         <p>系统运行时间:&nbsp;<strong>&nbsp;123&nbsp;</strong>天<strong>&nbsp;18&nbsp;</strong>时<strong>&nbsp;31&nbsp;</strong>分</br>恶意域名数总计:&nbsp;<strong>{{this.malTotal}}</strong></br> 检测日志数总计:&nbsp;<strong>{{this.logTotal}}</strong></p>
      </div>
    </main>
  </div>
</template>

<script>
import column from "@/components/column";
import line from "@/components/line";
import multipleColumn from "@/components/multipleColumn";
import point from "@/components/point";
import vmap from "@/components/map2";
import nav from "@/components/nav";
import { mapGetters } from "vuex";
import table from "@/components/table";
export default {
  data() {
    return {
      items: []
    };
  },
  computed: {
    ...mapGetters(["chart5Ydata", "dateYdata", "dateXdata", 'malTotal','logTotal'])
  },
  mounted() {},
  methods: {},
  components: {
    column,
    multipleColumn,
    point,
    "v-line": line,
    "v-nav": nav,
    "v-map": vmap,
    "v-table": table
  }
};
</script>

<style lang="scss" scoped>
* {
  box-sizing: border-box;
}

main {
  position: relative;
  height: calc(100% - 57px);
}
.item {
  position: absolute;
  a{
    z-index:100;
    font-size: 25px !important;
    position: absolute;
    right: 2em;
    bottom: 2em;
    color:#59aef5;
    font-size: 16px;
  }
}

.item.one {
  width: 100%;
  height: 100%;
  transform: translate(-25%, -22.5%) scale(0.5);
}
.item.two {
  width: 100%;
  height: 100%;
  transform: translate(-25%, 25%) scale(0.5);
}
.item.three {
  width: 100%;
  height: 100%;
  transform: translate(25%, 25%) scale(0.5);
}
.item.four{

  font-size:36px;
  padding: 50px 0 0 120px;
  width: 100%;
  height: 100%;
  transform: translate(24%, -22.5%) scale(0.5);
  h1{
    margin-top:2em;
    margin-bottom: 0.75em;
    font-size: 48px;
    font-weight: bold;
  }
  strong{
    color:red;
  }
  p{
    line-height: 1.6
  }
}

.dashboard {
  width: 100%;
  height: 100%;
  margin: 0px;
  padding: 0px;
  background-size: 100% 100%;
}
</style>