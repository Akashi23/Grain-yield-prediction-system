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
      <h1 class="d-flex justify-content-center crop">Количество урожая в тоннах в год</h1>
      <GChart
            type="ColumnChart"
            :data="crop"
            :options="chartOptions"
      />
      <div class="container">
        <div class="card-columns">
            <div class="card" style="display: contents" v-for="line in crops" :key="line.id">
              <div class="card-body">
                <h4 class="card-title">{{line[0][1]}}</h4>
                  <GChart
                        type="LineChart"
                        :data="line"
                        :options="chartOptions"
                  />
              </div>
            </div>
          </div>
        </div>
        <div class="container">
          <h1 class="d-flex justify-content-center crop">Почва в каждом Регионе Казахстана</h1>
          <table class="table table-bordered table-striped mb-0">
            <thead>
                <tr>
                    <th scope="col" v-for="columns in soils[0]" :key="columns.id">{{columns}}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="column in soils_all" :key="column.id">
                    <td scope="col" v-for="row in column" :key="row.id">{{row}}</td>
                </tr>
            </tbody>
        </table>   
      </div>
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
              this.crops = response.data.crops;
              this.soils = response.data.soils;
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
  data() {
    return {
      snow: null,
      precip:null,
      humidity:null,
      crop: null,
      crops: null,
      soils: null,
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
