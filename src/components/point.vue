<style lang="stylus" scoped>
.point {
  height: 100% !important;
  width: 100% !important;
  background: none !important;
  color: white;

  .main {
    width: 100%;
    height: calc(100% - 100px);
    margin-top: -15px;
  }
}
</style>

<template>
  <div class="point" ref="point">
    <v-header :name="name" :legendArr="legendArr" :myChart="myChart"></v-header>
    <div class="main"></div>
  </div>
</template>

<script>
import echarts from "echarts";
import header from "@/components/header";

export default {
  props: {
    title:String,
    chartData: Array
  },
  data() {
    return {
      legendArr: [],
      color: this.$store.state.color,
      myChart: {},
      name: this.title
    };
  },
  methods: {
    _init() {
      this.legendArr = this.myChart.getOption().series[0].data;

      this.legendArr.forEach(data => {
        data.selected = true;
      });
      this.$root.charts.push(this.myChart);
      window.addEventListener(
        "resize",
        function() {
          this.myChart.resize();
        }.bind(this)
      );
    }
  },
  components: {
    "v-header": header
  },
  mounted() {
    // 基于准备好的dom，初始化echarts实例
    this.myChart = echarts.init(this.$refs.point.querySelector(".point .main"));
    this.myChart.setOption({
      tooltip: {
        trigger: "item",
        formatter: "{a} <br/>{b} : {c} ({d}%)"
      },
      textStyle: {
        fontWeight: "normal",
        fontSize: 18
      },
      color: this.color,
      series: [
        {
          type: "pie",
          radius: "55%",
          center: ["50%", "60%"],
          data: this.chartData,
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)"
            }
          }
        }
      ]
    });
    this._init();
  }
};
</script>

