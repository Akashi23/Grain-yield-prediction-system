import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import PageNotFound from "./components/PageNotFound.vue"
import Predict from "./components/Predict.vue"
import Upload from "./components/Upload.vue"

Vue.use(VueRouter)


Vue.config.productionTip = false

const router = new VueRouter({
    routes: [
        { path: '/', component: Upload },
        { path: '/predict', component: Predict },
        { path: "*", component: PageNotFound }
    ]
})

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')