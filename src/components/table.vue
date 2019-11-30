<style lang="scss" scoped>
.table {
  height: 100% !important;
  width: 100% !important;
  background: none !important;
}

.main {
  width: 100%;
  height: calc(100% - 100px);
  margin-top: 50px;
}
p{
  line-height: 1.4;
  text-align: left;
  font-size: 20px !important;
  margin: -15px 0 15px 10px !important;
  strong{
   color:#e03e3e;
  }
}
button{
  float:right;
  transform: translate(-50%,-140%)
}
</style>
<style lang="scss" >
.el-table__body tr.hover-row>td{
    // background-color:#286595 !important;
}
.el-table__header {
  line-height: 40px !important ;
}
.el-table th,
.el-table tr {
  // background-color: #172c3b80;
}
.el-table {
  // color:#cecece;
  // background-color: #172c3b80;
  height: 100% !important;
  width: 600px;
  margin: 0 10px;
  padding: 10px;
  font-weight: bolder;
}
thead{
  color:black !important;
  font-weight: bolder;
}
.el-table td,
.el-table th.is-leaf {
  // border-bottom-color: #516593 !important;
}

.el-table__fixed-right::before, .el-table__fixed::before,.el-table::before{
    background-color: transparent
}

</style>


<template>
  <div class="table">
    <div class="main">
      <p>恶意域名数总计:&nbsp;<strong>{{this.malTotal}}</strong></br> 检测日志数总计:&nbsp;<strong>{{this.logTotal}}</strong></p>
       <el-button type="primary" round @click="xxx">ipv4/ipv6切换</el-button>
      <el-table :data="tableData" style="width: 100%" height="200" v-if="ipv4">
        <el-table-column fixed prop="ip" label="ipv4"></el-table-column>
        <el-table-column prop="domain" label="域名"></el-table-column>
        <el-table-column prop="time" label="时间"></el-table-column>
        <el-table-column prop="srcip" label="源ip"></el-table-column>
      </el-table>
      <el-table :data="tableDataIpv6" style="width: 100%" height="200" v-else>
        <el-table-column fixed prop="ip" label="ipv6"></el-table-column>
        <el-table-column prop="domain" label="域名"></el-table-column>
        <el-table-column prop="time" label="时间"></el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      tableData:this.$store.state.chartData.result,
      tableDataIpv6:this.$store.state.chartData.ipv6,
      ipv4:true
    };
  },
  computed: {
    ...mapGetters([
       'malTotal',
       'logTotal'
    ])
  },
  methods:{
    xxx(){
      console.log(this.ipv4,"ipv4");
      this.ipv4=!this.ipv4
    }
  },
  mounted(){
  }
};
</script>
    background-color: #172c3b80;