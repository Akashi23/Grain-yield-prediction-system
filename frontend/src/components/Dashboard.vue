<template>
<div>
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
      <h1 class="d-flex justify-content-center">Количество выпадение осадков в миллиметре в год</h1>
      <GChart
            type="ColumnChart"
            :data="precip"
            :options="chartOptions"
      />
      <h1 class="d-flex justify-content-center">Среднее значение влаги в процентах в год</h1>
      <GChart
            type="ColumnChart"
            :data="humidity"
            :options="chartOptions"
      />
      <h1 class="d-flex justify-content-center">Количество урожая в тоннах в год</h1>
      <GChart
            type="ColumnChart"
            :data="crop"
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
  name: "Dashboard",
  components: {
    GChart
  },
  mounted() {
      axios.get('http://localhost:8000/dashboard')
            .then((response) => {
              this.snow = response.data.snow;
              this.precip = response.data.precip;
              this.humidity = response.data.humidity;
              this.crop = response.data.crop;
            }).catch(error => {
              console.log(error)
              this.errored = true
            })
            .finally(() => this.loading = false)
  },
  data() {
    return {
      snow: null,
      precip:null,
      humidity:null,
      crop: null,
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
  font-size: 20px;
}
</style>
