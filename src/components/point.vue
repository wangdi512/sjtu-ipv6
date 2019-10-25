<style lang="stylus" scoped>
.point {
  height: 800px;
  background: url('../assets/bg.jpg') no-repeat;
  background-size: 100% 100%;
  color: white;

  .main {
    width: 100%;
    height: calc(100% - 100px);
    margin-top: -15px;
  }
}
</style>

<template>
  <div class="point">
    <v-header :name="name" :legendArr="legendArr" :myChart="myChart"></v-header>
    <div class="main"></div>
  </div>
</template>

<script>
import echarts from "echarts";
import header from "@/components/header";

export default {
  data() {
    return {
      legendArr: [],
      color: this.$store.state.color,
      myChart: {},
      name: "柱状图"
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
    }
  },
  components: {
    "v-header": header
  },
  mounted() {
    // 基于准备好的dom，初始化echarts实例
    this.myChart = echarts.init(document.querySelector(".point .main"));
    this.myChart.setOption({
      title: {
        text: "Customized Pie",
        left: "center",
        top: 20,
        textStyle: {
          color: "#ccc"
        }
      },

      tooltip: {
        trigger: "item",
        formatter: "{a} <br/>{b} : {c} ({d}%)"
      },

      visualMap: {
        show: false,
        min: 80,
        max: 600,
        inRange: {
          colorLightness: [0, 1]
        }
      },
      color:this.color,
      series: [
        {
          name: "访问来源",
          type: "pie",
          radius: "55%",
          center: ["50%", "50%"],
          data: [
            { value: 335, name: "直接访问" },
            { value: 310, name: "邮件营销" },
            { value: 274, name: "联盟广告" },
            { value: 235, name: "视频广告" },
            { value: 400, name: "搜索引擎" }
          ].sort(function(a, b) {
            return a.value - b.value;
          }),
          roseType: "radius",
          label: {
            normal: {
              textStyle: {
                color: "rgba(255, 255, 255, 0.3)"
              }
            }
          },
          labelLine: {
            normal: {
              lineStyle: {
                color: "rgba(255, 255, 255, 0.3)"
              },
              smooth: 0.2,
              length: 10,
              length2: 20
            }
          },
          itemStyle: {
            normal: {
              color: "#c23531",
              shadowBlur: 200,
              shadowColor: "rgba(0, 0, 0, 0.5)"
            }
          },

          animationType: "scale",
          animationEasing: "elasticOut",
          animationDelay: function(idx) {
            return Math.random() * 200;
          }
        }
      ]
    });
    this._init();
  }
};
</script>

