<template>
  <div>
    <section v-if="errored">
      <p>We're sorry, we're not able to retrieve this information at the moment, please try back later</p>
    </section>
    <section v-else>
    <div v-if="loading">
      <div class="d-flex justify-content-center"><h1 class="">Загрузка данных...</h1></div>
      <div class="d-flex justify-content-center"><img class="" src="https://flevix.com/wp-content/uploads/2019/12/Quarter-Circle-Loading-Image-1.gif" alt="this slowpoke moves"  width=250/></div>
      
    </div>
    <div v-else-if="loaded && loading == false">
      <div class="d-flex justify-content-center"><h1 class="">Загрузился</h1></div> 
    </div>
    <div class="container" v-else>
    <h1 class="d-flex justify-content-center">Загрузка статистических данных из stat.gov.kz</h1>
    <form class="d-flex justify-content-center" id="uploadForm" name="uploadForm" enctype="multipart/form-data">
      <input class="mt-5" type="file" id="files" name="files" multiple /><br />
      <input class="mt-5 ml-5" type="button" value="Upload" @click="this.uploadFiles" />
    </form>
    </div>
    </section>
  </div>
    
</template>
<script>
import axios from "axios";
export default {
  name: "Upload",
  data() {
    return {
      msg: null,
      loading: false,
      errored: false,
      loaded: false,
    };
  },
  methods: {
    uploadFiles() {
      const data = new FormData(document.getElementById("uploadForm"));
      var imagefile = document.querySelector("#files");
      console.log(imagefile.files[0]);
      data.append("file", imagefile.files[0]);
      this.loading = true;
      axios
        .post("http://localhost:8000/upload", data, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log(response);
          this.loading = false;
          this.loaded = true;
        })
        .catch((error) => {
          console.log(error.response);
        });
    },
  },
};
</script>