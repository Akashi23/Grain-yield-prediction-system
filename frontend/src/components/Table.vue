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
    <h3 class="p-3 text-center">Датасет урожайности зерновых культур в Казахстане</h3>
    <div class="table-wrapper-scroll-y my-custom-scrollbar">
        <table class="table table-bordered table-striped mb-0">
            <thead>
                <tr>
                    <th scope="col" v-for="columns in data_head" :key="columns.id">{{columns}}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="column in data_20" :key="column.id">
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
const axios = require('axios');
export default {
  name: "Table",
  components: {
  },
  mounted() {
      axios.get('http://localhost:8000/tables')
            .then((response) => {
              this.data = response.data.data
            }).catch(error => {
              console.log(error)
              this.errored = true
            })
            .finally(() => this.loading = false)
  },
  computed: {
      data_head () {
          return this.data[0]
      },
      data_20 () {
          return this.data.slice(1, 400)
      },
  },

  data() {
    return {
      data: null,
      loading: true,
      errored: false
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
tr {
    font-size: 13px;
}

table{
  padding: 40px;
}

.my-custom-scrollbar {
    position: relative;
    height:  500px;
    overflow: auto;
}
.table-wrapper-scroll-y {
    display: block;
}
/* .loading{
  padding-left: 40%;
} */
</style>
