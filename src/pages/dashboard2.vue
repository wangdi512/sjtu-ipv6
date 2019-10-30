<template>
  <div class="dashboard">
    <v-nav></v-nav>
    <div class="item one">
      <v-line
        title="一周内检测域名数变化"
        :xData="this.dateXdata"
        :yData="this.dateYdata"
        yName="数量/百条"
        xName="时间"
        :label="['检测域名数','检出恶意域名数']"
      ></v-line>
    </div>
    <div class="item two">
      <v-map></v-map>
    </div>
    <div class="item three">
      <v-table></v-table>-->
    </div>
  </div>
</template>

<script>
import column from "@/components/column";
import column2 from "@/components/column2";
import multipleColumn from "@/components/multipleColumn";
import point from "@/components/point";
import line from "@/components/line";
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
  mounted() {},
  methods: {},
  components: {
    column,
    column2,
    "v-line": line,
    multipleColumn,
    point,
    "v-nav": nav,
    "v-map": vmap,
    "v-table": table
  }
};
</script>

<style lang="stylus" scoped>
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
</style>