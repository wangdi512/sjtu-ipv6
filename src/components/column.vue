<style lang="stylus" scoped>
.columnChart {
  height: 100% !important;
  width: 100% !important;
  background: none !important;
  color: white;
}

.main {
  width: 100%;
  height: calc(100% - 100px);
  margin-top: -15px;
}
</style>

<template>
  <div class="columnChart" ref="column">
    <v-header :name="name" :legendArr="legendArr" :myChart="myChart"></v-header>
    <div class="main"></div>
  </div>
</template>

<script>
import echarts from "echarts";
import header from "@/components/header";

export default {
  props: {
    xData: Array,
    yData: Array,
    xName: String,
    yName: String,
    label: Array,
    title: String,
    barWidth: Number
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
    }
  },
  components: {
    "v-header": header
  },
  watch: {
    yData: function(val) {
      console.log(val, "!!");
      if (val&&val[0]) {
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
              type: "category",
              axisLine: {
                show: true
              },
              axisTick: {
                show: false
              },
              // nameTextStyle: {
              //   color: "rgba(255, 255, 255, 0.69)"
              // },
              axisLabel: {
                textStyle: {
                  // color: "white"
                  fontSize: 16
                }
              },
              data: this.xData
            }
          ],
          yAxis: [
            {
              axisLine: {
                show: true
              },
              nameLocation: "end",
              nameGap: 20,
              nameRotate: 0,
              axisTick: {
                show: false
              },
              splitLine: {
                // lineStyle: {
                //   color: ["rgba(230, 230, 230, 0.2)"]
                // }
              },
              axisLabel: {
                textStyle: {
                  color: "black",
                  fontSize: 16
                }
              },
              name: this.yName,
              type: "value"
              // nameTextStyle: {
              //   color: "rgba(255, 255, 255, 0.69)"
              // }
            }
          ],
          textStyle: {
            fontWeight: "normal",
            fontSize: 16,
          },
          series: this.label.map((v, i) => {
            return {
              name: v,
              type: "bar",
              data: val[i],
              barWidth: 35,
              barGap: 0,
              label: {
                normal: {
                  show: true,
                  color:"black",
                  position: "top"
                }
              }
            };
          })
        });
      }
    }
  },
  mounted() {
    // 基于准备好的dom，初始化echarts实例
    this.myChart = echarts.init(
      this.$refs.column.querySelector(".columnChart .main")
    );
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
          type: "category",
          axisLine: {
            show: true
          },
          axisTick: {
            show: false
          },
          // nameTextStyle: {
          //   color: "rgba(255, 255, 255, 0.69)"
          // },
          axisLabel: {
            textStyle: {
              // color: "white"
              fontSize: 16
            }
          },
          data: this.xData
        }
      ],
      yAxis: [
        {
          axisLine: {
            show: true
          },
          nameLocation: "end",
          nameGap: 20,
          nameRotate: 0,
          axisTick: {
            show: false
          },
          splitLine: {
            // lineStyle: {
            //   color: ["rgba(230, 230, 230, 0.2)"]
            // }
          },
          axisLabel: {
            textStyle: {
              color: "black",
              fontSize: 16
            }
          },
          name: this.yName,
          type: "value"
          // nameTextStyle: {
          //   color: "rgba(255, 255, 255, 0.69)"
          // }
        }
      ],
      textStyle: {
        fontWeight: "normal",
        fontSize: 16
      },
      series: this.label.map((v, i) => {
        return {
          name: v,
          type: "bar",
          data: this.yData[i],
          barWidth: 35,
          barGap: 0,
          label: {
            normal: {
              show: true,
              position: "insideTop"
            }
          }
        };
      })
    });
    this._init();
  },
  updated() {}
};
</script>
