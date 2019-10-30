
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
  watch: {
    yData: function(val) {
      this.myChart = echarts.init(
        this.$refs.column.querySelector(".columnChart .main")
      );
      if (val[0]) {
        console.log("!!!");
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
              // axisTick: {
              //   show: false
              // },
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
                lineStyle: {
                  color: ["rgba(230, 230, 230, 0.2)"]
                }
              },
              axisLabel: {
                textStyle: {
                  // color: "white",
                  fontSize: 16
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
            fontSize: 16
          },
          series: [
            {
              name: this.label[0],
              type: "bar",
              stack: "总量",
              data: [...val[0].slice(0, 4)],
              label: {
                normal: {
                  show: true,
                  position: "insideTop"
                }
              }
            },
            {
              name: this.label[1],
              type: "bar",
              stack: "总量",
              data: ["-", "-", "-", "-", ...val[0].slice(4, 8)],
              label: {
                normal: {
                  show: true,
                  position: "insideTop"
                }
              }
            }
          ]
        });
      }
    }
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
          // axisTick: {
          //   show: false
          // },
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
            lineStyle: {
              color: ["rgba(230, 230, 230, 0.2)"]
            }
          },
          axisLabel: {
            textStyle: {
              // color: "white",
              fontSize: 16
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
        fontSize: 16
      },
      series: [
        {
          name: this.label[0],
          type: "bar",
          stack: "总量",
          data: [...this.yData[0].slice(0, 4)],
          label: {
            normal: {
              show: true,
              position: "insideTop"
            }
          }
        },
        {
          name: this.label[1],
          type: "bar",
          stack: "总量",
          data: ["-", "-", "-", "-", ...this.yData[0].slice(4, 8)],
          label: {
            normal: {
              show: true,
              position: "insideTop"
            }
          }
        }
      ]
    });
    this._init();
  },
};
</script>
