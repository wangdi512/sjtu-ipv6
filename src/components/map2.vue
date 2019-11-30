<style lang="stylus" scoped>
.map {
  height: 100% !important;
  width: 100% !important;
  background: none !important;
  color: white;
}

.main {
  width: 100%;
  height: calc(100% - 100px);
  margin-top: 50px;
}
</style>

<template>
  <div class="map" ref="column">
    <!-- <v-header :name="name" :legendArr="legendArr" :myChart="myChart"></v-header> -->
    <div class="main"></div>
  </div>
</template>

<script>
import echarts from "echarts";
import header from "@/components/header";
import "echarts/map/js/world.js";
export default {
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
  mounted() {
    // 基于准备好的dom，初始化echarts实例
    this.myChart = echarts.init(this.$refs.column.querySelector(".map .main"));
    console.log(this.$store.state.chartData,"!!!!!!");
    this.myChart.setOption({
      //   backgroundColor: "#404a59",
      title: {
        text: "安全风险物联网设备全球标注图",
        left: "center",
        top: "top",
        textStyle: {
          // color: "#e0e6ef",
          fontSize:30
        }
      },
      tooltip: {
        trigger: "item",
        formatter: function(params) {
          return "ip地址:"+params.name;
        }
      },
      geo: {
        type: "map",
        map: "world",
        roam: false,
        label: {
          emphasis: {
            show: false
          }
        },
        itemStyle: {
          normal: {
            // areaColor: "#323c48", //区域颜色
            // borderColor: "#111" //区域划分边框颜色
          },
          emphasis: {
            // areaColor: "#2a333d" //鼠标Havor颜色
          }
        }
      },
      series: [
        {
          type: "effectScatter",
          coordinateSystem: "geo",
          data: this.$store.state.chartData.iot_message.slice(0,36).map(function(itemOpt) {
            return {
              name:itemOpt.ip=="2001:da8:8000:6026::200"? itemOpt.ip+"<br>"+"设备:"+itemOpt.device+"<br>"+"default_admin:admin" +"<br>"+"default_passwd:admin"+"<br>"+'devTypePattern :[[body, title], [regex, (?i)axis, (?i)router]]'+"<br>"+  "loginUrlPattern: document\\.write\\(\"([^\"\\]+)[^\\r\\n]+>Setup<\/a>" : itemOpt.ip+"<br>"+"设备:router"+"<br>"+ "devTypePattern: [[body, title], [regex, Basler AG]]"+"<br>"+"nextUrl: [string,  /cgi-bin/auth_if.cgi?Login ]"+"<br>"+ "auth: [form,  Auth.Username=admin&Auth.Password=admin, body, regex, success: true]",
              value: itemOpt.location,
              label: {
                normal: {
                  show: false,
                  position: "top",
                  formatter: "{b}",
                  textStyle: {
                    // color: "black",
                    fontWeight: "bold"
                  }
                }
              },
              symbolSize: 10,
              showEffectOn: "render",
              rippleEffect: {
                brushType: "stroke"
              },
              hoverAnimation: true,
              itemStyle: {
                normal: {
                  // color: "#ff3300",
                  shadowBlur: 10,
                  shadowColor: "red"
                }
              }
            };
          })
        }
      ]
    });
    this._init();
  }
};
</script>
