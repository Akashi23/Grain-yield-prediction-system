<template>
<div class="dashboard-class">
  <section v-if="errored">
    <p>We're sorry, we're not able to retrieve this information at the moment, please try back later</p>
  </section>

  <section v-else>
    <div class="d-flex justify-content-center" v-if="loading">
      <img src="http://i.stack.imgur.com/SBv4T.gif" alt="this slowpoke moves"  width=250/>
    </div>
    <div class="container" v-else>
      <h1 class="d-flex justify-content-center">Количество выпадение снега в сантиметрах в год</h1>
      <GChart
            type="ColumnChart"
            :data="snow"
            :options="chartOptions"
      />
      </div>
  </section>
</div>
</template>

<script>
import { GChart } from "vue-google-charts";
const axios = require('axios');
export default {
  name: "Predict",
  components: {
    GChart
  },
  mounted() {
      axios.get('http://localhost:8000/crop_test')
            .then((response) => {
              this.crops = response.data.crops;
            }).catch(error => {
              console.log(error)
              this.errored = true
            })
            .finally(() => this.loading = false)
  },
  computed: {
      soils_all() {
          return this.soils.slice(1, 18);
      },
  },
  method: {
      predict_data(){
           axios.post('http://localhost:8000/predict', this.predicted_data)
            .then((response) => {
              this.crops = response.data.crops;
            }).catch(error => {
              console.log(error)
              this.errored = true
            })
            .finally(() => this.loading = false);
      }
  },
  data() {
    return {
      crops: null,
      predicted_data: null,
      loading: true,
      errored: false,
      chartOptions: {
        chart: {
          title: "Snow",
          subtitle: "XZ"
        }
      }
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1{
  font-size: 26px;
}
.dashboard-class{
  padding-bottom: 100px;
}
.crop{
  padding-top: 100px;
  font: 2em sans-serif;
}
</style>
