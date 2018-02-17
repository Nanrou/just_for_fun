<template id="buildPc">

<el-row :gutter="10">
  <el-col :xs="6" :sm="6">
    <div style="height: 575px; padding-left: 15px">
      <!--
      <el-button @click="btnFakeDice">dice</el-button>
      <el-button @click="partOfAge = !partOfAge">age</el-button>
      <el-button @click="partOfJob = !partOfJob">job</el-button>
      <el-button @click="partOfSkill = !partOfSkill">skill</el-button>
      <el-button @click="partOfISkill = !partOfISkill">iSkill</el-button>
      -->
      <el-steps direction="vertical" :active="stepActive" finish-status="success">
        <el-step title="属性"></el-step>
        <el-step title="年龄"></el-step>
        <el-step title="职业"></el-step>
        <el-step title="技能"></el-step>
        <el-step title="特征"></el-step>
      </el-steps>
    </div>
  </el-col>

  <el-col :xs="18" :sm="18">
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
        <transition name="fade">
          <div style="padding-top: 10px" v-if="diceFinish">
            <el-button round type="success" @click="partOfDice=!partOfDice">下一步</el-button>
          </div>
        </transition>
      </el-card>
    </transition>

    <transition name="slide-fade" v-on:after-leave="stepMove">
      <el-card v-if="partOfAge" class="box-card">
        <div class="block">
          <h1>选择年龄</h1>
          <h2 v-if="ageConfirm">{{ age }}岁</h2>
          <el-slider :min="16" :max="99" v-model="age" :disabled="ageConfirm" show-input></el-slider>
          <transition name="fade">
            <div v-if="!ageConfirm">
              <div>
                <p>确定{{ age }}岁吗</p>
                <p>{{ ageText }}</p>
              </div>
              <el-button type="primary" plain @click="ageConfirm=!ageConfirm" >请谨慎决定喔</el-button>
            </div>
          </transition>
          <transition name="fade">
            <div v-if="ageConfirm">
              <div v-if="age < 20">
                <h2>属性调整</h2>
                <div>
                  <hr/>
                  <p>
                    <strong>力量</strong>和<strong>体型</strong>合计需要减去<strong>5</strong>点
                  </p>
                  <div>
                    <el-slider v-model="age20Punish" :min="0" :max="5" :format-tooltip="formatTooltipAge20"></el-slider>
                    <p>当前力量为{{ property[0].sum }}，调整后为{{ property[0].sum - age20Punish }}</p>
                    <p>当前体型为{{ property[1].sum }}，调整后为{{ property[1].sum - (5 - age20Punish) }}</p>
                  </div>
                </div>
                <div>
                  <hr>
                  <p>
                    <strong>教育</strong>需要减去<strong>5</strong>点，现在是<strong>{{ property[7].sum - 5}}</strong>点
                  </p>
                </div>
                <div>
                  <hr>
                  <p>
                    重掷<strong>幸运</strong>
                  </p>
                  <div v-if="age20ReRoll">
                    <div v-if="age20ReRollAction">
                      <img class="img-dice" src="../assets/dice/dice_action.gif" />
                      <img class="img-dice" src="../assets/dice/dice_action.gif" />
                      <img class="img-dice" src="../assets/dice/dice_action.gif" />
                    </div>
                    <div v-else>
                      <img v-for="dice of age20ReRollResult" class="img-dice" :src="dice" :key="dice.id"/>
                    </div>
                  </div>
                  <el-button v-if="!Boolean(age20ReRollResultText)" type="primary" plain @click="btnHandleAge20ReRoll">{{ age20ReRollText }}</el-button>
                  <p v-if="Boolean(age20ReRollResultText)">{{ age20ReRollResultText }}</p>
                </div>
              </div>
              <div v-else>
                <h2>属性调整</h2>
                <div v-if="Boolean(agePunish)">
                  <hr/>
                  <p>力量，体质，敏捷合计要减<strong>{{ agePunish }}</strong>点</p>
                  <div style="margin: 0 10px">
                    <div>
                      <div style="display: inline-block; width: 100%;">
                        <p style="float: left; font-size: 22px; margin: 4px"><strong>STR</strong></p>
                      </div>
                      <el-slider v-model="ageTmpSTR" :min="0" :max="agePunish"></el-slider>
                      <p style="margin: 4px">当前力量为{{ property[0].sum }}，调整后为{{ property[0].sum - ageTmpSTR }}</p>
                    </div>
                    <hr class="dashed" />
                    <div>
                      <div style="display: inline-block; width: 100%;">
                        <p style="float: left; font-size: 22px; margin: 4px"><strong>CON</strong></p>
                      </div>
                      <el-slider v-model="ageTmpCON" :min="0" :max="agePunish"></el-slider>
                      <p style="margin: 4px">当前体质为{{ property[1].sum }}，调整后为{{ property[1].sum - ageTmpCON }}</p>
                    </div>
                    <hr class="dashed" />
                    <div>
                      <div style="display: inline-block; width: 100%;">
                        <p style="float: left; font-size: 22px; margin: 4px"><strong>DEX</strong></p>
                      </div>
                      <el-slider v-model="ageTmpDEX" :min="0" :max="agePunish"></el-slider>
                      <p style="margin: 4px">当前敏捷为{{ property[3].sum }}，调整后为{{ property[3].sum - ageTmpDEX }}</p>
                    </div>
                  </div>
                  <div style="margin-top: 4px; font-size: 18px">{{ agePunishHelpText }}</div>
                </div>
                <div v-if="Boolean(agePunishApp)">
                  <hr/>
                  <div>
                    <p>
                      <strong>外貌</strong>需要减去<strong>{{ agePunishApp }}</strong>点，现在是<strong>{{ property[4].sum - agePunishApp }}</strong>点
                    </p>
                  </div>
                </div>
                <div>
                  <hr/>
                  <div>
                    <span style="margin-bottom: 4px">还可以进行<strong>{{ ageEDUTimes }}</strong>次教育增强鉴定</span>
                    <div style="width: 100%; height: 32px">
                      <el-button style="float: right; margin-right: 8px" size="small" type="info" round icon="el-icon-info" @click="btnAgeEDUNotice">关于教育增强鉴定</el-button>
                    </div>
                    <div style="font-size: 36px">DICE：{{ animateDice100Result }}</div>
                    <transition name="fade" mode="out-in">
                      <div v-if="Boolean(ageEDUTimes)" style="text-align: center">
                        <el-button type="primary" plain :disabled="btnAgeEDUDisabled" @click="btnHandleAgeEDU">{{ btnHandleAgeEDUText }}</el-button>
                      </div>
                      <div v-else>
                        <p style="font-size: 18px">最终，你的教育停留在<strong>{{ property[7].sum }}</strong>点</p>
                      </div>
                    </transition>
                  </div>
                </div>
              </div>
            </div>
          </transition>
          <transition name="fade">
            <div style="padding-top: 10px" v-if="ageFinish">
              <el-button round type="success" @click="btnHandleAgeNext">下一步</el-button>
            </div>
          </transition>
        </div>
      </el-card>
    </transition>

    <transition name="slide-fade" v-on:after-leave="stepMove">
      <el-card v-if="partOfJob" class="box-card">
        <div>
          <h1>确定职业</h1>
          <div>
            <el-select v-model="job" placeholder="请选择" value-key="职业">
              <el-option v-for="item in jobDetailData" :key="item['职业']" :label="item['职业']" :value="item">
              </el-option>
            </el-select>
          </div>
          <transition name="fade">
            <div v-if="job['细分']" style="margin-top: 8px">
              <hr class="dashed"/>
              <el-select v-model="jobItem" placeholder="请选择细分职业" value-key="职业">
                <el-option v-for="item in job['子类']" :key="item['职业']" :label="item['职业']" :value="item">
                </el-option>
              </el-select>
            </div>
          </transition>
          <transition name="fade">
            <div v-if="Boolean(job)" style="text-align: left">
              <p>职业描述：<span v-html="job['描述']"></span></p>
              <transition name="fade">
                <div v-if="!job['细分']">
                  <span>信用范围：{{ job['信用范围'] }}</span>
                  <el-button size="small" type="info" round icon="el-icon-info" @click="btnJobCreditNotice">信用是什么</el-button>
                  <p>技能点数：{{ job['本职技能点数'] }}</p>
                  <p>本职技能：{{ job['本职技能'] }}</p>
                </div>
                <div v-else-if="Boolean(jobItem)">
                  <span>信用范围：{{ jobItem['信用范围'] }}</span>
                  <el-button size="small" type="info" round icon="el-icon-info" @click="btnJobCreditNotice">信用是什么</el-button>
                  <p>技能点数：{{ jobItem['本职技能点数'] }}</p>
                  <p>本职技能：{{ jobItem['本职技能'] }}</p>
                </div>
              </transition>
            </div>
          </transition>
          <transition name="fade">
            <div v-if="jobFinish">
              <el-button round type="success" @click="partOfJob=!partOfJob">确定要当一个{{ jobTitle }}了吗</el-button>
            </div>
          </transition>
        </div>
      </el-card>
    </transition>

    <transition name="slide-fade" v-on:after-leave="partOfISkill = !partOfISkill">
      <el-card v-if="partOfSkill" class="box-card">
        <div>
          <div>
            <h2>调整技能</h2>
            <div>
              <p style="margin: 4px">本职技能点一共有<strong>{{ skillSumPoint }}</strong>点</p>
              <p style="margin: 4px" v-if="skillSumPoint > skillUsedPoint">还有{{ skillSumPoint - skillUsedPoint }}点待分配</p>
              <p style="margin: 4px" v-else-if="skillSumPoint < skillUsedPoint">不要太贪心啦，多出来的{{ skillUsedPoint - skillSumPoint }}点我怎么找给你喔</p>
              <p style="margin: 4px" v-else>调整完成</p>
            </div>
          </div>
          <div>
            <hr/>
            <div style="width: 100%;">
              <div style="height: 24px">
                <span style="float: left; font-size: 20px; margin: 2px"><strong>信用评级</strong></span>
                <el-button style="float: right" size="small" type="info" round icon="el-icon-info" @click="btnJobCreditNotice"></el-button>
              </div>
              <p style="text-align: left; margin: 4px; margin-top: 10px"><em>信用范围为：{{ skillCredit[0] }}-{{ skillCredit[1] }}</em></p>
              <p style="text-align: left; margin: 4px;"><em>已自动分配{{ skillCredit[0] }}点到信用评级上</em></p>
              <p style="text-align: left; margin: 4px;"><em>当前为：{{ skillCreditPoint }}点</em></p>
            </div>
            <div style="margin: 0 4px">
              <el-slider v-model="skillCreditPoint" :min="skillCredit[0]" :max="skillCredit[1]"></el-slider>
            </div>
          </div>
          <div style="width: 100%; height: 32px">
            <span style="float: left; font-size: 20px; margin: 2px"><em>技能点意味着什么</em></span>
            <el-button style="float: right" size="small" type="info" round icon="el-icon-info" @click="btnSkillPointNotice"></el-button>
          </div>
          <div v-for="(name, index) in jobSkill" :key="name.id">
            <hr/>
            <div style="width: 100%" v-if="skillSpecial[name] || name === '其他' || name instanceof Array">
              <el-select v-if="skillSpecial[name]" v-model="skill[index].name" placeholder="请选择">
                <el-option
                  v-for="s in skillSpecial[name]"
                  :key="s"
                  :label="s"
                  :value="s">
                </el-option>
              </el-select>
              <el-select v-else-if="name === '其他'" v-model="skill[index].name" placeholder="请选择">
                <el-option
                  v-for="s in skillNormal"
                  :key="s"
                  :label="s"
                  :value="s">
                </el-option>
              </el-select>
              <el-select v-else v-model="skill[index].name" placeholder="请选择">
                <el-option
                  v-for="s in name"
                  :key="s"
                  :label="s"
                  :value="s">
                </el-option>
              </el-select>
              <div v-if="name !== skill[index].name">
                <div style="width: 100%;">
                  <div style="height: 24px; margin-top: 8px">
                    <span style="float: left; font-size: 20px; margin: 2px"><strong>{{ skill[index].name }}</strong></span>
                    <el-button style="float: right" size="small" type="info" round icon="el-icon-info" @click="btnSkillNotice(skill[index].name)"></el-button>
                  </div>
                  <p style="text-align: left; margin: 4px; margin-top: 10px"><em>技能初始值为：{{ skillDefaultData[skill[index].name] }}，当前为{{ skill[index].point }}</em></p>
                </div>
                <div style="margin: 0 4px">
                  <el-slider show-input v-model="skill[index].point" :min="skillDefault(skill[index].name)" :max="90"></el-slider>
                </div>
              </div>
            </div>
            <div v-else>
              <div style="width: 100%;">
                <div style="height: 24px">
                  <span style="float: left; font-size: 20px; margin: 2px"><strong>{{ skill[index].name }}</strong></span>
                  <el-button style="float: right" size="small" type="info" round icon="el-icon-info" @click="btnSkillNotice(skill[index].name)"></el-button>
                </div>
                <p style="text-align: left; margin: 4px; margin-top: 10px"><em>技能初始值为：{{ skillDefaultData[skill[index].name] }}，当前为{{ skill[index].point }}</em></p>
              </div>
              <div style="margin: 0 4px">
                <el-slider show-input v-model="skill[index].point" :min="skillDefault(skill[index].name)" :max="90"></el-slider>
              </div>
            </div>
          </div>
        </div>
        <transition name="fade">
          <div v-if="skillFinish">
            <el-button round type="success" @click="btnHandleSkillNext">确定这样分配了吗</el-button>
          </div>
        </transition>
      </el-card>
    </transition>

    <transition name="slide-fade" v-on:after-leave="stepMove">
      <el-card v-if="partOfISkill">
        <div class="box-card">
          <h2>选择兴趣技能</h2>
          <div>
            <div>
              <p style="margin: 4px">兴趣技能点一共有<strong>{{ iSkillSumPoint }}</strong>点</p>
              <p style="margin: 4px" v-if="iSkillSumPoint > iSkillUsedPoint">还有{{ iSkillSumPoint - iSkillUsedPoint }}待分配</p>
              <p style="margin: 4px" v-else-if="iSkillSumPoint < iSkillUsedPoint">不要太贪心啦，多出来的{{ iSkillUsedPoint - iSkillSumPoint }}点我怎么找给你喔</p>
              <p style="margin: 4px" v-else>调整完成</p>
            </div>
            <hr/>
          </div>
          <div>
            <p>加感兴趣的技能就好</p>
            <p>温馨提示:<em>专精好过什么都懂一点</em></p>
          </div>
          <div v-for="(item, index) of iSkill" :key="item.id">
            <hr/>
            <div>
              <el-select v-model="iSkill[index].name" placeholder="请选择">
                <el-option
                  v-for="s in skillNormal"
                  :key="s"
                  :label="s"
                  :value="s">
                </el-option>
              </el-select>
              <div v-if="iSkill[index].name !== ''">
                <div style="width: 100%;">
                  <div style="height: 24px; margin-top: 8px">
                    <span style="float: left; font-size: 20px; margin: 2px"><strong>{{ iSkill[index].name }}</strong></span>
                    <el-button style="float: right" size="small" type="info" round icon="el-icon-info" @click="btnSkillNotice(iSkill[index].name)"></el-button>
                  </div>
                  <p style="text-align: left; margin: 4px; margin-top: 10px"><em>技能初始值为：{{ skillDefaultData[iSkill[index].name] }}，当前为{{ iSkill[index].point }}</em></p>
                </div>
                <div style="margin: 0 4px">
                  <el-slider show-input v-model="iSkill[index].point" :min="skillDefault(iSkill[index].name)" :max="90"></el-slider>
                </div>
              </div>
            </div>
          </div>
          <div style="height: 40px; margin: 4px; margin-top: 10px">
            <el-button style="float: left" round type="success" :disabled="this.iSkillSumPoint !== this.iSkillUsedPoint" @click="btnHandleISkillNext">确定这样分配了吗</el-button>
            <el-button style="float: right" @click="btnHandleISkillAppend">+</el-button>
          </div>
        </div>
      </el-card>
    </transition>

    <transition name="slide-fade" v-on:after-leave="stepMove">
      <el-card v-if="partOfFeature">
        <div class="box-card">
          <div>
            <h3>决定名字</h3>
            <el-input v-model="name" :maxlength="10" placeholder="请输入内容"></el-input>
          </div>
          <hr/>
          <div>
            <h3>选择性别</h3>
            <el-select v-model="sex" placeholder="请选择">
              <el-option
                v-for="s in sexRange"
                :key="s"
                :label="s"
                :value="s">
              </el-option>
            </el-select>
          </div>
          <div v-for="value in feature" :key="value.id">
            <hr/>
            <div style="width: 100%;">
              <div style="height: 24px; margin-top: 8px">
                <span style="float: left; font-size: 20px; margin: 2px"><strong>{{ value.message }}</strong></span>
              </div>
              <el-select v-model="value.value" placeholder="请选择">
                <el-option
                  v-for="s in value.range"
                  :key="s"
                  :label="s"
                  :value="s">
                  <span>{{ s.slice(0, s.indexOf('。')) }}</span>
                </el-option>
              </el-select>
              <p><em>{{ value.value }}</em></p>
            </div>
            <div style="margin: 10px 4px">
              <el-input v-model="value.detail" :maxlength="32" placeholder="尝试去丰满背景"></el-input>
            </div>
          </div>
        </div>
        <transition name="fade">
          <div v-if="featureFinish">
            <el-button round type="success" @click="btnHandleFinal">确定好了吗</el-button>
          </div>
        </transition>
      </el-card>
    </transition>

  </el-col>
</el-row>

</template>

<script>
import ElContainer from 'element-ui/packages/container/src/main'
import ElCard from 'element-ui/packages/card/src/main'

import TWEEN from 'tween.js'
import axios from 'axios'

export default {
  components: {
    ElCard,
    ElContainer
  },
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
      ageDetailData: require('../assets/data/age_data'),
      ageConfirm: false,
      age20Punish: 0,
      age20ReRoll: false,
      age20ReRollAction: true,
      age20ReRollText: 'Re-roll',
      age20ReRollResult: [],
      age20ReRollResultText: 0,
      // 20岁以上的
      agePunish: 0,
      agePunishApp: 0,
      ageEDUTimes: 1,
      btnAgeEDUDisabled: false,
      dice100Result: 0,
      animateDice100Result: 0,
      btnHandleAgeEDUText: '看一下岁月是否有使你进步',
      ageTmpSTR: 0,
      ageTmpCON: 0,
      ageTmpDEX: 0,

      partOfJob: false,
      job: '',
      jobItem: '',
      jobDetailData: require('../assets/data/job_data').data,

      partOfSkill: false,
      skillCreditPoint: 0,
      skillDefaultData: require('../assets/data/skill_data').skillDefaultPoint,
      skillSpecial: {
        '社交': require('../assets/data/skill_data').skillSocial,
        '科学': require('../assets/data/skill_data').skillScience,
        '艺术/手艺': require('../assets/data/skill_data').skillArt,
        '生存': require('../assets/data/skill_data').skillSurvive,
        '学术': require('../assets/data/skill_data').skillAcademic,
        '驾驶': require('../assets/data/skill_data').skillDrive,
        '格斗': require('../assets/data/skill_data').skillFight,
        '射击': require('../assets/data/skill_data').skillShot,
        '外语': require('../assets/data/skill_data').skillOtherLanguage
      },
      skillNormal: require('../assets/data/skill_data').skillNormal,
      skillNoticeData: require('../assets/data/skill_data').skillDetail,
      skill: [{'name': '', 'point': 0}, {'name': '', 'point': 0}, {'name': '', 'point': 0}, {'name': '', 'point': 0}, {'name': '', 'point': 0}, {'name': '', 'point': 0}, {'name': '', 'point': 0}, {'name': '', 'point': 0}],

      partOfISkill: false,
      iSkill: [{'name': '', 'point': 0}],
      finalSkill: {},

      partOfFeature: false,
      name: '',
      sex: '',
      sexRange: ['男', '女', '双性人', '变性人(男变女)', '变性人(女变男)'],

      feature: {
        'faith': {
          'message': '选择信仰方向',
          'range': require('../assets/data/feature_data').faith,
          'detail': '',
          'value': ''
        },
        'lover': {
          'message': '选择心爱之人',
          'range': require('../assets/data/feature_data').lover,
          'detail': '',
          'value': ''
        },
        'loverReason': {
          'message': '选择羁绊原因',
          'range': require('../assets/data/feature_data').lover_reason,
          'detail': '',
          'value': ''
        },
        'importantPlace': {
          'message': '选择意义非凡之地',
          'range': require('../assets/data/feature_data').impressive_place,
          'detail': '',
          'value': ''
        },
        'treasure': {
          'message': '选择宝贵之物',
          'range': require('../assets/data/feature_data').treasure,
          'detail': '',
          'value': ''
        }
      }

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
        case 4:
          this.partOfFeature = true
          break
      }
    },

    showMultiNotice (title, texts) {
      const h = this.$createElement
      let tmpArray = []
      for (let item of texts) {
        tmpArray.push(h('p', { style: 'margin: 2px 0' }, item))
      }

      this.$notify.info({
        title: title,
        position: 'top-left',
        dangerouslyUseHTMLString: true,
        message: h('div', { style: 'color: teal; font-size: 16px' }, tmpArray)
      })
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

    formatTooltipAge20 (value) {
      return '力量减去' + value + '点，体质减去' + (5 - value) + '点'
    },

    initAgePunish (punish, app, eduTimes) {
      this.agePunish = punish
      this.agePunishApp = app
      this.ageEDUTimes = eduTimes
    },

    btnHandleAge20ReRoll () {
      if (this.age20ReRoll) {
        this.age20ReRollAction = false
        let sum = 0
        for (let j = 0; j < 3; j++) {
          let res = Math.floor(Math.random() * 6) + 1
          this.age20ReRollResult.push(require('../assets/dice/dice_' + res + '.png'))
          sum += res * 5
        }
        if (this.property[8].sum < sum) {
          this.property[8].sum = sum
          this.age20ReRollResultText = '看来幸运女神对你再次露出了微笑，现在你的幸运为' + this.property[8].sum
        } else {
          this.age20ReRollResultText = '看来幸运女神并不在这里，现在你的幸运还是' + this.property[8].sum
        }
      } else {
        this.age20ReRoll = true
        this.age20ReRollText = 'Stop'
      }
    },

    btnAgeEDUNotice () {
      const h = this.$createElement
      this.$notify.info({
        title: '教育增强鉴定',
        position: 'top-left',
        message: h('i', { style: 'color: teal; font-size: 16px' }, '教育增强鉴定是指掷100面骰子，若结果比当前教育点数高，则可以增加1D10的点数')
      })
    },

    btnHandleAgeEDU () {
      this.dice100Result = Math.floor(Math.random() * 100)
      this.btnHandleAgeEDUText = '再' + this.btnHandleAgeEDUText

      let msg
      if (this.dice100Result > this.property[7].sum) {
        let point = Math.ceil(Math.random() * 10)
        this.property[7].sum += point
        msg = '看来岁月的流逝让你获得了不少知识，你的EDU提高了' + point + '点，现在是' + this.property[7].sum + '点了'
      } else {
        msg = '看来你并没有从岁月的流逝中获得什么知识，你的EDU还停留在' + this.property[7].sum
      }

      const h = this.$createElement
      this.$notify.info({
        title: '教育增强鉴定结果',
        position: 'top-left',
        message: h('i', { style: 'color: teal; font-size: 16px' }, msg)
      })

      this.ageEDUTimes--
      this.btnAgeEDUDisabled = !this.btnAgeEDUDisabled
      setTimeout(
        () => {
          this.btnAgeEDUDisabled = !this.btnAgeEDUDisabled
        },
        800
      )
    },

    btnHandleAgeNext () {
      if (this.age < 20) {
        this.property[0].sum -= this.age20Punish
        this.property[1].sum -= (5 - this.age20Punish)
        this.property[7].sum -= 5
      } else {
        this.property[0].sum -= this.ageTmpSTR
        this.property[1].sum -= this.ageTmpCON
        this.property[3].sum -= this.ageTmpDEX
        this.property[4].sum -= this.agePunishApp
      }
      this.partOfAge = false

      this.skillDefaultData['闪避'] = Math.floor(this.property[3].sum / 2)
      this.skillDefaultData['母语'] = this.property[7].sum
    },

    btnJobCreditNotice () {
      let jobCreditText = [
        '信用评级表现出一个人的日常生活水平，以及相关社会身份和地位，简单点说就是有多少钱。',
        '信用评级0:身无分文。连贫穷都够不上的人才能够叫做身无分文。',
        '信用评级1-9:贫穷。刚好买得起最廉价的屋顶，每天能够吃到一餐廉价食物。',
        '信用评级10-49:标准。舒适的生活水平，一日三餐，偶尔下馆子。',
        '信用评级50-89:小康。小康级别已经可以享受奢侈品的舒适了。',
        '信用评级90+:富裕。富裕级别就是享受超级奢侈品的时候了。',
        '信用评级99:豪富。钱已经只是一个代号了，是世界上最富有的人之一。'
      ]
      this.showMultiNotice('信用评级', jobCreditText)
    },

    calculateSkillPoint (pro, time) {
      let sum = 0
      for (let i in this.property) {
        if (this.property[i].description.indexOf(pro) > -1) {
          sum = this.property[i].sum * time
          break
        }
      }
      return sum
    },

    btnSkillPointNotice () {
      let skillText = [
        '1-5:新手:完全的外行人。',
        '6-19:初学者:拥有少量知识的初学者。',
        '20-49:业余:拥有一定程度的天赋或者基本的训练(兴趣爱好程度)。',
        '50-74:职业:允许一名角色凭借此技能来谋生。等同于特定领域的学士学位。',
        '75-89:专家:在专业知识上更进一步。相当于硕士或者博士学位。',
        '90+:大师:位列于该技能的世界顶尖人物之列。'
      ]
      this.showMultiNotice('技能点意味着什么', skillText)
    },

    initSkill (skills) {
      let i = 0
      for (let skill of skills) {
        this.skill[i].name = skill
        i++
      }
    },

    btnSkillNotice (name) {
      if (this.skillNoticeData.hasOwnProperty(name)) {
        this.showMultiNotice(name, this.skillNoticeData[name])
      } else {
        const h = this.$createElement
        this.$notify.info({
          title: name,
          position: 'top-left',
          message: h('i', { style: 'color: teal; font-size: 16px' }, '问KP')
        })
      }
    },

    skillDefault (name) {
      if (this.skillDefaultData.hasOwnProperty(name)) {
        return parseInt(this.skillDefaultData[name])
      } else {
        return 0
      }
    },

    btnHandleSkillNext () {
      for (let item of this.skill) {
        this.skillDefaultData[item.name] = item.point
      }
      this.partOfSkill = false
    },

    btnHandleISkillAppend () {
      this.iSkill.push({'name': '', 'point': 0})
    },

    btnHandleISkillNext () {
      for (let item of this.skill) {
        this.finalSkill[item.name] = item.point
      }
      for (let item of this.iSkill) {
        this.finalSkill[item.name] = item.point
      }
      this.partOfISkill = false
    },

    btnFakeDice () {
      for (let item of this.property) {
        item.sum = 60
      }
      this.partOfDice = !this.partOfDice
    },

    btnHandleFinal () {
      let finalData = {}
      finalData['name'] = this.name
      finalData['sex'] = this.sex
      finalData['property'] = {}
      for (let item of this.property) {
        finalData['property'][item.type] = item.sum
      }
      finalData['age'] = this.age
      finalData['job'] = this.jobTitle
      finalData['credit'] = this.skillCreditPoint
      finalData['skill'] = this.finalSkill
      for (let item in this.finalSkill) {
        finalData['skill'][item] = this.finalSkill[item]
      }
      finalData['feature'] = {}
      for (let key in this.feature) {
        finalData['feature'][key] = this.feature[key].detail ? this.feature[key].detail : this.feature[key].value
      }

      console.log(finalData)
      axios.post('/api/create', finalData)
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
  },

  computed: {
    diceFinish () {
      for (let item of this.property) {
        if (!item.dice_lock) {
          return false
        }
      }
      return true
    },

    ageText () {
      if (this.age < 20) {
        return this.ageDetailData['19']
      } else if (this.age < 40) {
        this.initAgePunish(0, 0, 1)
        return this.ageDetailData['39']
      } else if (this.age < 50) {
        this.initAgePunish(5, 5, 2)
        return this.ageDetailData['49']
      } else if (this.age < 60) {
        this.initAgePunish(10, 10, 3)
        return this.ageDetailData['59']
      } else if (this.age < 70) {
        this.initAgePunish(20, 15, 4)
        return this.ageDetailData['69']
      } else if (this.age < 80) {
        this.initAgePunish(40, 20, 4)
        return this.ageDetailData['79']
      } else {
        this.initAgePunish(80, 25, 4)
        return this.ageDetailData['89']
      }
    },

    agePunishHelpText () {
      let tmpSum = this.ageTmpSTR + this.ageTmpCON + this.ageTmpDEX
      if (tmpSum < this.agePunish) {
        return '还要减去 ' + (this.agePunish - tmpSum) + ' 点属性点才够呢'
      } else if (tmpSum > this.agePunish) {
        return '别减太多，会死的'
      } else {
        return '调整完成'
      }
    },

    ageFinish () {
      if (this.ageEDUTimes === 0) {
        if (this.age < 20 && Boolean(this.age20ReRollResultText)) {
          return true
        } else if (this.agePunish === this.ageTmpDEX + this.ageTmpSTR + this.ageTmpCON) {
          return true
        }
      }
      return false
    },

    jobTitle () {
      if (!this.job['细分']) {
        return this.job['职业']
      } else if (this.jobItem) {
        return this.jobItem['职业']
      }
    },

    jobFinish () {
      if (this.job) {
        if (!this.job['细分']) {
          return true
        } else if (this.jobItem) {
          return true
        }
      }
      return false
    },

    skillCredit () {
      let creditText = !this.job['细分'] ? this.job['信用范围'] : this.jobItem['信用范围']
      let min, max, tmp
      tmp = creditText.split('-')
      min = parseInt(tmp[0])
      max = parseInt(tmp[1])
      return [min, max]
    },

    skillSumPoint () {
      let pointText = !this.job['细分'] ? this.job['本职技能点数'] : this.jobItem['本职技能点数']

      let sum = 0
      let pro, time, tmp
      if (pointText.indexOf('+') < 0) {
        tmp = pointText.split('×')
        pro = tmp[0]
        time = parseInt(tmp[1])
        sum = this.calculateSkillPoint(pro, time)
      } else {
        let part1, part2
        tmp = pointText.split('+')
        part1 = tmp[0]
        part2 = tmp[1]
        let tmp2 = part1.split('×')
        pro = tmp2[0]
        time = parseInt(tmp2[1])
        sum += this.calculateSkillPoint(pro, time)

        if (part2.indexOf('或')) {
          let tmp2 = part2.split('×')
          let part3 = tmp2[0]
          time = parseInt(tmp2[1])

          let tmp3 = part3.split('或')
          let pro1 = tmp3[0]
          let pro2 = tmp3[1]

          let tmpSum1 = this.calculateSkillPoint(pro1, time)
          let tmpSum2 = this.calculateSkillPoint(pro2, time)

          sum += tmpSum1 > tmpSum2 ? tmpSum1 : tmpSum2
        } else {
          let tmp2 = part2.split('×')
          pro = tmp2[0]
          time = parseInt(tmp2[1])
          sum += this.calculateSkillPoint(pro, time)
        }
      }
      return sum
    },

    skillUsedPoint () {
      let sum = 0
      sum += this.skillCreditPoint
      for (let item of this.skill) {
        sum += item.point - this.skillDefault(item.name)
      }
      return sum
    },

    jobSkill () {
      let mapper = require('../assets/data/skill_data').skillMapper
      let skills = mapper[this.jobTitle]
      this.initSkill(skills)
      return skills
    },

    skillFinish () {
      for (let item of this.skill) {
        if (item.point === 0) {
          return false
        }
      }
      if (this.skillSumPoint === this.skillUsedPoint) {
        return true
      }
    },

    iSkillSumPoint () {
      return this.property[7].sum * 2
    },

    iSkillUsedPoint () {
      let sum = 0
      for (let item of this.iSkill) {
        if (item.point === 0) {
          break
        }
        sum += item.point - this.skillDefault(item.name)
      }
      return sum
    },

    featureFinish () {
      if (this.name && this.sex) {
        for (let index in this.feature) {
          if (!this.feature[index].value) {
            return false
          }
        }
        return true
      }
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
    },

    job: function (newValue, oldValue) {
      this.jobItem = null
    }

  }

}
</script>

<style>
  .box-card {
    width: 100%;
    /*height: 575px;*/
  }

  .el-card__body {
    padding: 10px;
  }

  .el-table .cell {
   padding-left: 6px;
  }

  .img-dice {
    width: 90px;
    height: 90px;
  }

  hr {
    margin-top: 5px;
    margin-bottom: 2px;
    border: 0;
    height: 2px;
    background-image: -webkit-linear-gradient(left, #f0f0f0, #666666, #f0f0f0);
    background-image: -moz-linear-gradient(left, #f0f0f0, #666666, #f0f0f0);
  }

  .dashed {
    border: 0;
    height: 0;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  }

  .fixed-skill-header {
    position: fixed;
    width: 248px;
    height: 105px;
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

  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }
</style>
