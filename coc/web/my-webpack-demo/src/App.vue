<template>
  <div id="app">
    <p>
      <router-link to="Home">Go to Home</router-link>
      <router-link to="About">Go to About</router-link>
      <router-link to="build_pc">Go to BuildPc</router-link>
    </p>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 30px;
  height: 600px;
  width: 360px;
}
</style>
