import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Table from "./components/Table.vue"
import PageNotFound from "./components/PageNotFound.vue"
import Dashboard from "./components/Dashboard.vue"
import Predict from "./components/Predict.vue"
import Upload from "./components/Upload.vue"

Vue.use(VueRouter)


Vue.config.productionTip = false

const router = new VueRouter({
    routes: [
        { path: '/', component: Table },
        { path: '/dashboard', component: Dashboard },
        { path: '/predict', component: Predict },
        { path: '/upload', component: Upload },
        { path: "*", component: PageNotFound }
    ]
})

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')