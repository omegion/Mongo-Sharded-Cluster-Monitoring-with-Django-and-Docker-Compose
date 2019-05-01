window.Vue = require('vue');
window.moment = require('moment');
window.axios = require('axios');
window.axios.defaults.xsrfCookieName = 'csrftoken'
window.axios.defaults.xsrfHeaderName = 'X-CSRFToken'
window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

import _ from 'lodash'


// Vue Router
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import Buefy from 'buefy'

// Teams
import ReplicasIndex from './components/replicas/Index.vue';

// 
// Vue.use
Vue.use(Buefy, {
  defaultToastDuration: 3000,
})

Vue.mixin({
    components: {
      // Teams
      'replicas-index': ReplicasIndex,
    },
});

var vm = new Vue({
  el: '#app',
});