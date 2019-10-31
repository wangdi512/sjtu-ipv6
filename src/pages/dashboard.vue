<template>
  <div class="dashboard">
    <v-nav></v-nav>
    <div class="item one">
      <point :chartData="this.chart3Data" title="IPv4/IPv6流量占比图"></point>
     
    </div>
    <div class="item two">
      <column2
        title="IPV4/IPV6各服务总流量大小"
        xName="服务"
        yName="byte数"
        :xData="['http','ipv4_ftp','ipv4_smtp','ipv4_dns','http','ipv6_ftp','ipv6_smtp','ipv6_dns']"
        :label="[ 'ipv4' ,'ipv6']"
        :yData="this.ydata2"
      ></column2>
    </div>
    <div class="item three">
      <v-line
        title="IPv4/IPv6流量变化折线图"
        :xData="this.chart1Xdata"
        :yData="this.ydata3"
        yName="流量大小/byte"
        xName="时间/s"
        :label="['ipv4','ipv6']"
      ></v-line>
    </div>
    <div class="item four">
      <v-line
        title="IPv4/IPv6上下行流量变化折线图"
        :xData="this.chart2Xdata"
        :yData="this.ydata4"
        yName="流量大小/byte"
        xName="时间/s"
        :label="['ipv4上行','ipv4下行','ipv6上行','ipv6下行']"
      ></v-line>
    </div>
    <div class="item five">
       <column
        title="IPv6各服务提供商上下行流量大小"
        xName="服务商"
        yName="流量大小/Byte"
        :xData="['教育网','电信', '联通','移动','阿里d','腾讯','亚马逊']"
        :label="[ '上行流量','下行流量' ]"
        :yData="this.data5"
      ></column>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import column from "@/components/column";
import column2 from "@/components/column2";
import line from "@/components/line";
import multipleColumn from "@/components/multipleColumn";
import point from "@/components/point";
import nav from "@/components/nav";
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      items: [],
      top: [2000, 2000, 2000, 2000, 2000],
      windowHeight: 768
    };
  },
  computed: {
    ...mapGetters([
      "chart1Ydata",
      "chart1Xdata",
      "chart2Ydata",
      "chart2Xdata",
      "chart3Data",
      "chart4Ydata",
      "chart5Ydata"
    ]),
    ydata2() {
      return this.top[1] < this.windowHeight - 300 ? this.chart4Ydata : [];
    },
    ydata3() {
      return this.top[2] < this.windowHeight - 300 ? this.chart1Ydata : [];
    },
    ydata4() {
      return this.top[3] < this.windowHeight - 300 ? this.chart2Ydata : [];
    },
    data5() {
      return this.top[4] < this.windowHeight - 300 ? this.chart5Ydata : [];
    }
  },
  mounted() {
    this.windowHeight = window.innerHeight;
    Vue.nextTick(() => {
      this.top = [].slice.call(document.querySelectorAll(".item")).map(e => {
        return e.getBoundingClientRect().top;
      });
      window.addEventListener("scroll", () => {
        this.top = [].slice.call(document.querySelectorAll(".item")).map(e => {
          return e.getBoundingClientRect().top;
        });
      });
    });
  },
  methods: {},
  components: {
    column2,
    column,
    multipleColumn,
    point,
    "v-line": line,
    "v-nav": nav
  }
};
</script>

<style lang="scss" scoped>
* {
  box-sizing: border-box;
}

.item {
  padding: 10px 0;
  margin: auto auto !important;
  width: 80%;
  height: 100%;
  text-align: center;
  transition: all 0.8s;
}

.dashboard {
  position: relative;
  width: 100%;
  height: 100%;
  margin: 0px;
  padding: 0px;
  background-size: 100% 100%;
}

.item.one {
  height: 100%;
}
// .flex-container.column {
//   flex-basis: 100%;
//   flex-direction: column;
//   flex-wrap: no-wrap;
//   // padding-top: 25px;
//   margin: auto;
//   position: relative;
//   height: calc(100vh - 57px);
//   width: 90%;
//   margin: 0 auto 0 auto;
//   box-sizing: content-box;
// }
</style>