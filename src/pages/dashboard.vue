<template>
  <div class="dashboard">
    <v-nav></v-nav>
    <div class="flex-container column">
      <div
        class="item one"
        @click="clickChart('1')"
        style="transform: translate(-22.4%,-38%) scale(0.22)"
      >
        <column
          title="图5"
          xName="服务"
          yName="流量"
          :xData="['教育网','电信', '联通','移动','阿里d','腾讯','亚马逊']"
          :label="[ '上行流量','下行流量' ]"
          :yData="this.chart5Ydata"
        ></column>
      </div>
      <div
        class="item two"
        @click="clickChart('2')"
        style="transform: translate(-22.4%,-13%) scale(0.22)"
      >
        <column
          title="图4"
          xName="服务"
          yName="byte数"
          :xData="['ipv4_http','ipv4_ftp','ipv4_smtp','ipv4_dns','ipv6_http','ipv6_ftp','ipv6_smtp','ipv6_dns']"
          :label="[ '服务Byte数' ]"
          :yData="this.chart4Ydata"
        ></column>
      </div>
      <div
        class="item three"
        @click="clickChart('3')"
        style="transform: translate(-22.4%,12%) scale(0.22)"
      >
        <v-line
          title="图1"
          :xData="this.chart1Xdata"
          :yData="this.chart1Ydata"
          yName="数量"
          xName="时间"
          :label="['ipv4','ipv6']"
        ></v-line>
      </div>
      <div
        class="item three"
        @click="clickChart('4')"
        style="transform: translate(-22.4%,37%) scale(0.22)"
      >
        <v-line
          title="图2"
          :xData="this.chart2Xdata"
          :yData="this.chart2Ydata"
          yName="数量"
          xName="时间"
          :label="['ipv4上行','ipv4下行','ipv6上行','ipv6下行']"
        ></v-line>
      </div>
      <div
        class="item four active"
        @click="clickChart('5')"
        style="transform: translate(43.7%, 0) scale(1)"
      >
        <point :chartData="this.chart3Data" title="图3"></point>
      </div>
    </div>
  </div>
</template>

<script>
import column from "@/components/column";
import line from "@/components/line";
import multipleColumn from "@/components/multipleColumn";
import point from "@/components/point";
import nav from "@/components/nav";
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      items: []
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
    ])
  },
  mounted() {
    this._init();
  },
  methods: {
    _resize() {
      this.$root.charts.forEach(myChart => {
        myChart.resize();
      });
    },
    _init() {
      this.items = document.querySelectorAll(".flex-container .item");
      for (let i = 0; i < this.items.length; i++) {
        this.items[i].dataset.order = i + 1;
      }
    },
    clickChart(clickIndex) {
      let activeItem = document.querySelector(".flex-container .active");
      let activeIndex = activeItem.dataset.order;
      let clickItem = this.items[clickIndex - 1];
      if (activeIndex === clickIndex) {
        return;
      }
      activeItem.classList.remove("active");
      clickItem.classList.add("active");
      this._setStyle(clickItem, activeItem);
    },
    _setStyle(el1, el2) {
      let transform1 = el1.style.transform;
      let transform2 = el2.style.transform;
      el1.style.transform = transform2;
      el2.style.transform = transform1;
    }
  },
  components: {
    column,
    multipleColumn,
    point,
    "v-line": line,
    "v-nav": nav
  }
};
</script>

<style lang="stylus" scoped>
* {
  box-sizing: border-box;
}

.item {
  padding: 0px;
  margin: 0px;
  width: 68%;
  height: 100%;
  position: absolute;
  transform: scale(0.33);
  text-align: center;
  transition: all 0.8s;
  background: rgba(32, 32, 35, 0.5);
}

.dashboard {
  position: relative;
  width: 100%;
  height: 100%;
  margin: 0px;
  padding: 0px;
  background: url('../assets/bg.jpg');
  background-size: 100% 100%;
}

.flex-container.column {
  padding-top: 25px;
  margin: auto;
  position: relative;
  height: 85%;
  width: 90%;
  overflow: hidden;
  margin: 0 auto 0 auto;
  box-sizing: content-box;
}

.active {
  height: 100%;
  width: 69%;
  margin-left: 10px;
  line-height: 300px;
}
</style>