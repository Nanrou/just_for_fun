<template id="buildPc">
  <el-row :gutter="10">
    <el-col :xs="6" :sm="6">
      <div style="height: 575px; padding-left: 15px">
        <el-button @click="partOfDice = !partOfDice">dice</el-button>
        <el-button @click="partOfAge = !partOfAge">age</el-button>
        <el-button @click="partOfJob = !partOfJob">job</el-button>
        <el-steps direction="vertical" :active="stepActive" finish-status="success">
          <el-step title="属性"></el-step>
          <el-step title="年龄"></el-step>
          <el-step title="职业"></el-step>
          <el-step title="技能"></el-step>
          <el-step title="特征"></el-step>
        </el-steps>
      </div>
    </el-col>
    <el-col :xs="18" :sm="18" style="height: 575px">
      <transition name="slide-fade" appear v-on:after-leave="stepMove">
        <el-card v-if="partOfDice" id="card-dice" class="box-card">
          <div v-if="diceAction">
            <img class="img-dice" src="../assets/dice/dice_action.gif" />
            <img class="img-dice" src="../assets/dice/dice_action.gif" />
            <img class="img-dice" src="../assets/dice/dice_action.gif" />
          </div>
          <div v-else>
            <img v-for="dice of diceResult" class="img-dice" :src="dice" :key="dice.id"/>
          </div>
          <el-table :data="property" style="width: 100%" height="335" @row-click="showPropertyDetail">
            <el-table-column label="属性">
              <template slot-scope="scope">
                <span style="float: left;">{{ scope.row.type }}-{{ scope.row.description }}</span>
              </template>
            </el-table-column>
            <el-table-column label="" >
              <template slot-scope="scope">
                <span style="float: right">
                  <el-button size="small" :disabled="scope.row.dice_lock" @click="btnHandleDice(scope.$index)">{{ scope.row.status }}</el-button>
                </span>
              </template>
            </el-table-column>
          </el-table>
          <div style="padding-top: 10px">
            <el-button round type="success" :disabled="diceNextDisabled" @click="partOfDice=!partOfDice">下一步</el-button>
          </div>
        </el-card>
      </transition>

      <transition name="slide-fade" v-on:after-leave="stepMove">
        <el-card v-if="partOfAge">
          <div class="block">
            <h1>选择年龄</h1>
            <el-slider :min="16" :max="99" v-model="age" @change="sliderHandleAge"></el-slider>
            <div>
              <p>确定{{ age }}岁吗</p>
              <p>{{ ageText }}</p>
            </div>
            <el-button type="primary" plain>请谨慎决定喔</el-button>
          </div>
        </el-card>
      </transition>

      <transition name="slide-fade" v-on:after-leave="stepMove">
        <el-card v-if="partOfJob">cccccc</el-card>
      </transition>

      <transition name="slide-fade" v-on:after-leave="stepMove">
        <el-card v-if="partOfSkill">dddddd</el-card>
      </transition>

    </el-col>
  </el-row>
</template>

<script>
import ElContainer from 'element-ui/packages/container/src/main'
import ElCard from 'element-ui/packages/card/src/main'

export default {
  components: {
    ElCard,
    ElContainer},
  data: function () {
    return {
      stepActive: 0,

      partOfDice: true,
      diceAction: false,
      diceResult: [require('../assets/dice/dice_1.png'), require('../assets/dice/dice_1.png'), require('../assets/dice/dice_1.png')],
      property: [
        { description: '力量(3D6)', sum: 0, type: 'str', status: 'Roll', dice_lock: false },
        { description: '体质(3D6)', sum: 0, type: 'con', status: 'Roll', dice_lock: false },
        { description: '体型(3D6)', sum: 0, type: 'siz', status: 'Roll', dice_lock: false },
        { description: '敏捷(3D6)', sum: 0, type: 'dex', status: 'Roll', dice_lock: false },
        { description: '外貌(3D6)', sum: 0, type: 'app', status: 'Roll', dice_lock: false },
        { description: '意志(3D6)', sum: 0, type: 'pow', status: 'Roll', dice_lock: false },
        { description: '智力(2D6+6)', sum: 0, type: 'int', status: 'Roll', dice_lock: false },
        { description: '教育(2D6+6)', sum: 0, type: 'edu', status: 'Roll', dice_lock: false },
        { description: '幸运(3D6)', sum: 0, type: 'luck', status: 'Roll', dice_lock: false }
      ],
      propertyDetail: require('../assets/data/property_data'),

      partOfAge: false,
      age: 32,
      ageDetail: require('../assets/data/age_data'),

      partOfJob: false,

      partOfSkill: false
    }
  },

  methods: {
    stepMove () {
      this.stepActive++
      switch (this.stepActive) {
        case 1:
          this.partOfAge = true
          break
        case 2:
          this.partOfJob = true
          break
        case 3:
          this.partOfSkill = true
          break
      }
    },

    btnHandleDice (index) {
      this.diceAction = !this.diceAction
      if (this.diceAction) {
        for (let i in this.property) {
          if (parseInt(i) === index) {
            this.property[i].status = 'Stop'
          } else {
            this.property[i].dice_lock = true
          }
        }
      } else {
        for (let i in this.property) {
          if (parseInt(i) === index) {
            let sum = 0
            if (this.property[i].type === 'int' || this.property[i].type === 'edu') {
              for (let j = 0; j < 2; j++) {
                let res = Math.floor(Math.random() * 6) + 1
                this.diceResult[j] = require('../assets/dice/dice_' + res + '.png')
                sum += res
              }
              this.diceResult[2] = require('../assets/dice/dice_6.png')// 手动调整最后一个骰子
              sum += 6
            } else {
              for (let j = 0; j < 3; j++) {
                let res = Math.floor(Math.random() * 6) + 1
                this.diceResult[j] = require('../assets/dice/dice_' + res + '.png')
                sum += res
              }
            }
            this.property[i].sum = this.property[i].status = sum * 5
            this.property[i].dice_lock = true
          } else {
            if (this.property[i].sum === 0) {
              this.property[i].dice_lock = false
            }
          }
        }
      }
    },

    showPropertyDetail (row, event, column) {
      if (parseInt(row.sum) !== 0) {
        const h = this.$createElement
        let tmpArray = []
        for (let item of this.propertyDetail[row.type]) {
          tmpArray.push(h('p', { style: 'margin: 2px 0' }, item))
        }

        this.$notify({
          title: row.description.slice(0, 2) + '说明',
          dangerouslyUseHTMLString: true,
          message: h('div', { style: 'color: teal; font-size: 16px' }, tmpArray),
          position: 'top-left'
        })
      }
    },

    sliderHandleAge (value) {
      this.age = value
    }

  },

  computed: {
    diceNextDisabled () {
      for (let item of this.property) {
        if (!item.dice_lock) {
          return true
        }
      }
      return false
    },

    ageText () {
      if (this.age < 19) {
        return this.ageDetail['19']
      } else if (this.age < 39) {
        return this.ageDetail['39']
      } else if (this.age < 49) {
        return this.ageDetail['49']
      } else if (this.age < 59) {
        return this.ageDetail['59']
      } else if (this.age < 69) {
        return this.ageDetail['69']
      } else if (this.age < 79) {
        return this.ageDetail['79']
      } else {
        return this.ageDetail['89']
      }
    }
  }

}
</script>

<style>
  .box-card {
    width: 100%;
  }

  .img-dice {
    width: 80px;
    height: 80px;
  }

  .slide-fade-enter-active {
    transition: all .5s ease;
  }
  .slide-fade-leave-active {
    transition: all .8s cubic-bezier(1.0, 0.5, 0.8, 1.0);
  }
  .slide-fade-enter, .slide-fade-leave-to
    /* .slide-fade-leave-active for below version 2.1.8 */ {
    transform: translateX(10px);
    opacity: 0;
  }

</style>
