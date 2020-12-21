<template>
  <div id="app">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <Navbar />
    {{insert}}
    <router-view></router-view>
  </div>
</template>

<script>
//import Table from "./components/Table.vue"
import Navbar from "./components/Navbar.vue"

export default {
  name: 'App',
  components: {
 //   Table,
    Navbar
  },
  computed:{
    insert(){
      let recaptchaScript = document.createElement('script')
      recaptchaScript.setAttribute('src', 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js')
      recaptchaScript.setAttribute('integrity', 'sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q')
      recaptchaScript.setAttribute('crossorigin', 'anonymous')
      let script = document.createElement('script')
      script.setAttribute('src', 'https://code.jquery.com/jquery-3.2.1.slim.min.js')
      script.setAttribute('integrity', 'sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN')
      script.setAttribute('crossorigin', 'anonymous')
      let recaptcha = document.createElement('script')
      recaptcha.setAttribute('src', 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js')
      recaptcha.setAttribute('integrity', 'sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl')
      recaptcha.setAttribute('crossorigin', 'anonymous')
      if(document.body != null){
        document.body.appendChild(recaptchaScript)
        document.body.appendChild(script)
        document.body.appendChild(recaptcha)
      }
      return ""
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 0;
}
</style>
