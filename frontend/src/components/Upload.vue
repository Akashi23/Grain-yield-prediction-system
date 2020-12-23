<template>
  <div>
    <h1 class="d-flex justify-content-center">Загрузка статистических данных из stat.gov.kz</h1>
    <form class="d-flex justify-content-center" id="uploadForm" name="uploadForm" enctype="multipart/form-data">
      <input class="mt-5" type="file" id="files" name="files" multiple /><br />
      <input class="mt-5 ml-5" type="button" value="Upload" @click="this.uploadFiles" />
    </form>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "Upload",
  data() {
    return {
      msg: null,
    };
  },
  methods: {
    uploadFiles() {
      const data = new FormData(document.getElementById("uploadForm"));
      var imagefile = document.querySelector("#files");
      console.log(imagefile.files[0]);
      data.append("file", imagefile.files[0]);

      axios
        .post("http://localhost:8000/upload", data, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error.response);
        });
    },
  },
};
</script>