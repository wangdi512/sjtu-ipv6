<template>
  <div class="dashboard">
    <v-nav></v-nav>
    <div class="item  one" style="transform:  scale(1)">
      <v-map></v-map>
      
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
  mounted() {},
  methods: {},
  components: {
    column,
    multipleColumn,
    point,
    "v-line": line,
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