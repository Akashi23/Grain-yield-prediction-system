<template>
<div>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="/">Crop Project</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <router-link class="nav-link" :to="{ path: '/' }">Home</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" :to="{ path: 'dashboard' }">Dashboard</router-link>
        <!--<a class="nav-link" href="/dashboard">Dashboard</a> -->
      </li>
    </ul>
  </div>
</nav>
</div>
</template>

<script>
export default {
    
}
</script>