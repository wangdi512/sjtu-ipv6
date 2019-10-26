<!-- 层叠柱状图 -->
<style lang="stylus" scoped>
.line {
  height: 100% !important;
  width: 100% !important;
  background: none !important;
}

.main {
  width: 100%;
  height: calc(100% - 100px);
  margin-top: -15px;
}
</style>

<template>
  <div class="line" ref="line">
    <v-header :name="name" :legendArr="legendArr" :myChart="myChart"></v-header>
    <div class="main"></div>
  </div>
</template>

<script>
import echarts from "echarts";
import header from "@/components/header";

export default {
  props: {
    title: String,
    xName: String,
    yName: String,
    label: Array,
    xData: Array,
    yData: Array
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
      this.legendArr = this.myChart.getOption().series;
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
    },
    getSeries() {}
  },
  components: {
    "v-header": header
  },
  mounted() {
    // 基于准备好的dom，初始化echarts实例
    this.myChart = echarts.init(this.$refs.line.querySelector(".line .main"));
    this.myChart.setOption({
      title: {
        show: false
      },
      tooltip: {
        trigger: "axis"
      },
      legend: {
        show: false
      },
      toolbox: {
        show: false
      },
      color: this.color,
      calculable: true,
      xAxis: [
        {
          name: this.xName,
          // type: "category",
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          nameTextStyle: {
            color: "rgba(255, 255, 255, 0.69)"
          },
          axisLabel: {
            textStyle: {
              color: "white"
            }
          },
          data: this.xData
        }
      ],
      yAxis: [
        {
          axisLine: {
            show: false
          },
          nameLocation: "end",
          nameGap: 20,
          nameRotate: 0,
          axisTick: {
            show: false
          },
          splitLine: {
            lineStyle: {
              color: ["rgba(230, 230, 230, 0.2)"]
            }
          },
          axisLabel: {
            textStyle: {
              color: "white",
              fontSize: 14
            }
          },
          name: this.yName,
          type: "value",
          nameTextStyle: {
            color: "rgba(255, 255, 255, 0.69)"
          }
        }
      ],
      textStyle: {
        fontWeight: "normal",
        fontSize: 18
      },
      series: this.label
        ? this.label.map((v, i) => {
            return {
              name: v,
              type: "line",
              stack: "总量",
              data: this.yData[i]
            };
          })
        : { name: "", type: "line", stack: "总量", data: [] }
    });
    this._init();
  }
};
</script>
