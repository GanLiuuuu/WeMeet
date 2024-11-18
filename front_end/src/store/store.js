// store.js
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    dstIp: null,
    dstPort: null,
  },
  mutations: {
    setConnection(state, { ip, port }) {
      state.dstIp = ip;
      state.dstPort = port;
    },
  },
  actions: {
    saveUserConnection({ commit }, { ip, port }) {
      commit('setConnection', { ip, port });
    },
  },
});