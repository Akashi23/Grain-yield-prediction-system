<template>
  <div class="dashboard-class">
    <section v-if="errored">
      <p>
        We're sorry, we're not able to retrieve this information at the moment,
        please try back later
      </p>
    </section>

    <section v-else>
      <div class="d-flex justify-content-center" v-if="loading">
        <img
          src="http://i.stack.imgur.com/SBv4T.gif"
          alt="this slowpoke moves"
          width="250"
        />
      </div>
      <div class="container" v-else>
        <div class="container">
          <h1 class="d-flex justify-content-center crop">Данные для теста</h1>
          <div class="table-wrapper-scroll-y my-custom-scrollbar">
            <table class="table table-bordered table-striped mb-0">
              <thead>
                <tr>
                  <th
                    scope="col"
                    v-for="columns in test_show[0]"
                    :key="columns.id"
                  >
                    {{ columns }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="column in test_all" :key="column.id">
                  <td scope="col" v-for="row in column" :key="row.id">
                    {{ row }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <button type="button" class="btn btn-primary ml-5 mt-5" v-on:click="predict_data(test_x)">Предсказать</button>
        <div class="d-flex justify-content-center">
         <div class="card ">
          <div class="card-body">
            <h5 class="card-title">Предсказание</h5>
            <p class="card-text"><div class="">Тестовая значение {{test_y[0]}}</div>
        <div class="">Предсказанные значение {{crops}}</div>
          </div>
          <div class="card-footer">
            <small class="text-muted"></small>
          </div>
         </div>
      </div>
      </div>
    </section>
  </div>
</template>

<script>
// import { GChart } from "vue-google-charts";
const axios = require("axios");
export default {
  name: "Predict",
  components: {
    // GChart
  },
  mounted() {
    axios
      .get("http://localhost:8000/crop_test")
      .then((response) => {
        this.test_show = response.data.test_show;
        this.test_x = response.data.test_x;
        this.test_y = response.data.test_y;
      })
      .catch((error) => {
        console.log(error.response);
        this.errored = true;
      })
      .finally(() => (this.loading = false));
  },
  computed: {
    test_all() {
      return this.test_show.slice(1, 2);
    },
  },
  methods: {
    predict_data: function (data) {
      axios
        .post("http://localhost:8000/predict", data)
        .then((response) => {
          this.crops = response.data.predicted;
          console.log(this.crops);
        })
        .catch((error) => {
          console.log(error.response);
        });
    },
  },
  data() {
    return {
      crops: null,
      test_show: null,
      test_x: null,
      test_y: null,
      predicted_data: null,
      loading: true,
      errored: false,
      chartOptions: {
        chart: {
          title: "Snow",
          subtitle: "XZ",
        },
      },
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-size: 26px;
}
.dashboard-class {
  padding-bottom: 100px;
}
.crop {
  padding-top: 100px;
  font: 2em sans-serif;
}
.my-custom-scrollbar {
  position: relative;
  overflow: auto;
}
.table-wrapper-scroll-y {
  display: block;
}
</style>
