<template>
  <div style="margin-top: 60px">
    <p>决定命运的时候到啦</p>
    <p style="font-size: 88px;margin: 16px;">{{ animateDice100Result }}</p>
    <transition name="fade">
      <div v-if="showDice">
        <el-button type="primary" @click="rollDice">ROLL</el-button>
      </div>
    </transition>
    <div style="margin-top: 30px">
      <img src="../assets/lulu.png"/>
    </div>
  </div>
</template>

<script>
import TWEEN from 'tween.js'

export default {
  data: function () {
    return {
      dice100Result: 0,
      animateDice100Result: 0,
      showDice: true
    }
  },

  methods: {
    rollDice () {
      this.dice100Result = Math.floor(Math.random() * 100)
      this.showDice = false
      setTimeout(
        () => {
          if (Math.floor(Math.random() * 10) < 9) {
            this.dice100Result = Math.floor(Math.random() * 100)
          }
        },
        800
      )
      setTimeout(
        () => {
          this.showDice = true
        },
        5000
      )
    }
  },

  watch: {
    dice100Result: function (newValue, oldValue) {
      let vm = this
      function animate () {
        if (TWEEN.update()) {
          requestAnimationFrame(animate)
        }
      }

      new TWEEN.Tween({ tweeningNumber: oldValue })
        .easing(TWEEN.Easing.Quadratic.Out)
        .to({ tweeningNumber: newValue }, 500)
        .onUpdate(function () {
          vm.animateDice100Result = this.tweeningNumber.toFixed(0)
        })
        .start()

      animate()
    }
  }

}
</script>

<style>
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }
</style>
