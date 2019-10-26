<template>
  <div class="dashboard">
    <v-nav></v-nav>
    <div class="flex-container column">
      <div
        class="item four active"
        style="transform:  scale(1)"
      >
      <v-map></v-map>
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
import vmap from "@/components/map2";
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
  },
  methods: {
   
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
  display :flex;
  justify-content :center
}

.active {
  height: 100%;
  width: 69%;
  margin-left: 10px;
  line-height: 300px;
}
</style>