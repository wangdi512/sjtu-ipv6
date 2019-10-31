<style lang="scss" scoped>
.point {
  height: 100% !important;
  width: 100% !important;
  background: none !important;
  position: relative;

  .main {
    width: 100%;
    height: calc(100% - 100px);
    margin-top: -15px;
  }
  p {
    position: absolute !important;
    left: 19px;
    top: 70px;
    line-height: 1.4;
    text-align: left;
    strong {
      color: #e03e3e;
    }
  }
}
</style>

<template>
  <div class="point" ref="point">
    <v-header :name="name" :legendArr="legendArr" :myChart="myChart" :headerColor="this.color"></v-header>
    <p>
      本日监控流量总大小为
      <strong>{{this.chartData[0].value+this.chartData[1].value}}</strong>Byte</br>其中IPv4流量总大小为
      <strong>{{this.chartData[0].value}}</strong> Bytes</br>IPv6流量总大小为
      <strong>{{this.chartData[1].value}}</strong>Byte</br。
    </p>
    <div class="main"></div>
  </div>
</template>

<script>
import echarts from "echarts";
import header from "@/components/header";

export default {
  props: {
    title: String,
    chartData: Array
  },
  data() {
    return {
      legendArr: [],
      color: ["#AE5548", "#6D9EA8", "#325B69", "#698570", "#9CC2B0", "#C98769"],
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
  watch: {
    chartData: function(val) {
     this.myChart = echarts.init(
        document.querySelector(".point .main")
      ); 
      if (val[0]) {
        console.log(">?????", this.myChart, val);
        this.myChart.setOption({
          tooltip: {
            trigger: "item",
            formatter: "{b} : {c} ({d}%)"
          },
          textStyle: {
            fontWeight: "normal",
            fontSize: 20
          },
          color: this.color,
          series: [
            {
              type: "pie",
              radius: "55%",
              center: ["50%", "60%"],
              data: val,
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
      }
    }
  },
  mounted() {
    // 基于准备好的dom，初始化echarts实例
    this.myChart = echarts.init(this.$refs.point.querySelector(".point .main"));
    this.myChart.setOption({
      tooltip: {
        trigger: "item",
        formatter: "{b} : {c} ({d}%)"
      },
      textStyle: {
        fontWeight: "normal",
        fontSize: 20
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

