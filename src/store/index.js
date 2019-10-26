import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const state = {
  count: 0,
  color: ['#325B69', '#698570', '#AE5548', '#6D9EA8', '#9CC2B0', '#C98769'],
  chartData: {}
};

const mutations = {
  initData(state, payload) {
    state.chartData = payload;
  }
};
const getters = {
  chart1Ydata: state => {
    return Object.values(state.chartData.chart1).reduce(
      (acc, v) => {
        acc[0].push(v[0]);
        acc[1].push(v[1]);
        return acc;
      },
      [[], []]
    );
  },
  chart1Xdata: state => {
    return Object.keys(state.chartData.chart1);
  },
  chart2Ydata: state => {
    return Object.values(state.chartData.chart2).reduce(
      (acc, v) => {
        acc[0].push(v[0]);
        acc[1].push(v[1]);
        acc[2].push(v[2]);
        acc[3].push(v[3]);
        return acc;
      },
      [[], [], [], [], []]
    );
  },
  chart2Xdata: state => {
    return Object.keys(state.chartData.chart2);
  },
  chart3Data: state => {
    return [
      { value: state.chartData.chart3[0], name: "ipv4" },
      { value: state.chartData.chart3[1], name: "ipv6" }
    ];
  },
  chart4Ydata: state => {
    return [state.chartData.chart4];
  },
  chart5Ydata: state => {
    return [state.chartData.chart5.slice(0,7),state.chartData.chart5.slice(7,14)];
  }
};

export default new Vuex.Store({
  state,
  mutations,
  getters
});
