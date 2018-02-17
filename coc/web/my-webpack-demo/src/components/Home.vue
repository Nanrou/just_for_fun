<template id="home">
    <div>
      <p>Home page</p>
      <input v-model="name"/>
      <el-button @click="getPc">get pc</el-button>
      <div v-if="getDataSuccess">
        <p>姓名: {{data.name}}</p>
        <p>性别: {{data.sex}}</p>
        <p>年龄：{{data.age}}</p>
        <p>职业: {{data.job}}</p>
        <p>信用评级: {{data.credit}}</p>
        <div>
          <p>属性</p>
          <p v-for="(value, key) of data.property" :key="key.id">
            {{ key }}: {{ value }}
          </p>
        </div>
        <div>
          <p>技能</p>
          <p v-for="(value, key) of data.skill" :key="key.id">
            {{ key }}: {{ value }} / {{ Math.floor(value / 2) }} / {{ Math.floor(value / 4) }}
          </p>
        </div>
        <div>
          <p>特征</p>
          <p v-for="(value, key) of data.feature" :key="key.id">
            {{ key }}: {{ value }}
          </p>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  data: function () {
    return {
      randomNumber: 0,
      name: '',
      data: {},
      getDataSuccess: false
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
    },

    getPc () {
      axios.get('/api/get/' + this.name, {})
        .then(
          response => {
            this.getDataSuccess = true
            this.data = response.data.data
            console.log(response)
          }
        ).catch(
          error => {
            console.log(error)
          }
        )
    },

    postPcToBackend () {
      let data = {name: 'test', data: 'data'}
      axios.post('/api/create', data)
        .then(
          response => {
            console.log('success', response)
          })
        .catch(
          error => {
            console.log(error)
          }
        )
    }
  }

}
</script>
