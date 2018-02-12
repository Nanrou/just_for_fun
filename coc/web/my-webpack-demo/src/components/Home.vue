<template id="home">
    <div>
      <p>Home page</p>
      <p>Random number from backend: {{ randomNumber }}</p>
      <el-button @click="getRandom">New random number</el-button>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  data: function () {
    return {
      randomNumber: 0
    }
  },

  methods: {

    getRandom () {
      this.randomNumber = this.getRandomFromBackend()
    },

    getRandomFromBackend () {
      const path = '/api/random'
      // const path = 'http://coc.dananrou.dev:8079/api/random'
      axios.get(path, {
      }).then(
        response => {
          this.randomNumber = response.data.randomNumber
        }
      ).catch(
        error => {
          console.log(error)
        }
      )
    }
  }

}
</script>
