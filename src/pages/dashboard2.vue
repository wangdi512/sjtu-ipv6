<template>
  <div class="dashboard">
    <v-nav></v-nav>
    <div class="flex-container column">
      <div
        class="item one"
        @click="clickChart('1')"
        style="transform: translate(-22.4%,-33.5%) scale(0.33)"
      >
        <v-map></v-map>
      </div>
      <div
        class="item two"
        @click="clickChart('2')"
        style="transform: translate(-22.4%,0.5%) scale(0.33)"
      >
        <v-table></v-table>
      </div>
      <div
        class="item three"
        @click="clickChart('3')"
        style="transform: translate(-22.4%,34.5%) scale(0.33)"
      >
       
      </div>
      <div
        class="item four active"
        @click="clickChart('4')"
        style="transform: translate(43.7%, 0) scale(1)"
      >
       <v-line
          title="图2"
          :xData="this.dateXdata"
          :yData="this.dateYdata"
          yName="数量"
          xName="时间"
          :label="['malcount','logcount']"
        ></v-line>
        <!-- <point></!--> -->
      </div>
    </div>
  </div>
</template>

<script>
import column from "@/components/column";
import line from "@/components/line";
import multipleColumn from "@/components/multipleColumn";
import point from "@/components/point";
import vmap from "@/components/map";
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
    ...mapGetters(["dateYdata", "dateXdata"])
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
    "v-nav": nav,
    "v-map": vmap,
    "v-table":table
  }
};
</script>

<style lang="stylus" scoped>
* {
  box-sizing: border-box;
}

.point, .multipleColumn, .columnChart, .line {
  height: 100% !important;
  width: 100% !important;
  background: none !important;
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