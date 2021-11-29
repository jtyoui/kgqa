<template>
  <div class="box">
    <el-container class="bg">

      <el-header class="head">
        <img class="logoIcon" :src="logoHead" alt="用户">
        <div class="title">作物病虫害智能问答系统</div>
      </el-header>

      <el-container style="height: 80%">
        <el-main id="scrollText">

          <div class="chat" v-for="msg of content">
            <div class="right cams" v-if="msg.people">
              <img class="headIcon radius" :src="peopleHead" alt="用户">
              <span class="name">
              <span class="title">用 户</span>
            </span>
              <span class="content"> {{ msg.people }} </span>
            </div>

            <div class="left cams" v-if="msg.robot">
              <img class="headIcon radius" :src="robotHead" alt="小智机器人"/>
              <span class="name">
                <span class="title">小智机器人</span>
              </span>
              <span class="content">{{ msg.robot }}</span>
            </div>

            <el-card class="box-card" v-if="msg.sentence.length !==0" shadow="never">
              <template #header>
                <span>{{ msg.greetings }}</span>
              </template>
              <div v-for="(recommend,index) of msg.sentence" :key="recommend" class="text item">
                {{ index + 1 }}、{{ recommend }}
                <hr/>
              </div>
            </el-card>

          </div>
        </el-main>
      </el-container>

      <el-footer>
        <el-input :prefix-icon="Search" class="input" placeholder="请输入一句话" v-model="people" @keydown.enter="onSubmit"
                  clearable>
          <template #append>
            <el-button type="success" @click="onSubmit" :icon="Message" auto-insert-space>发送</el-button>
          </template>
        </el-input>
      </el-footer>

    </el-container>
  </div>
</template>


<script setup>
import axios from 'axios'
import {nextTick, onMounted, reactive, ref} from "vue";
import {Message, Search} from '@element-plus/icons'

const robotHead = ref("")
const peopleHead = ref("")
const logoHead = ref("")

const content = reactive([
  {
    "people": "",
    "robot": "🙂嗨，我是您的智能机器人小智，可以为您解答作物病虫害领域的问题哦~",
    "sentence": [],
    "greetings": ""
  }])
const people = ref("")

function onSubmit() {
  axios.get("/wss/qa?question=" + people.value).then(data => {
    console.log(data.data)
    if (data.data.code === 200) {
      let value = ""
      data.data.data.forEach(v => {
        value = value + "、" + v;
      })
      const result = {
        "people": people.value,
        "robot": value.substr(1),
        "sentence": data.data.sentence,
        "greetings": "👇 还为您找到以下类似问题哦：",
      }
      content.push(result)
      people.value = ""
      nextTick(() => {
        const scroll = document.getElementById('scrollText')
        scroll.scrollTop = scroll.scrollHeight
      })
    } else if (data.data.code === 201) {
      const result = {
        "people": people.value,
        "robot": "",
        "sentence": data.data.sentence,
        "greetings": "💔 非常抱歉，小智没有找到您想要的答案呢，您可以这样问试试：",
      }
      content.push(result)
      people.value = ""
      nextTick(() => {
        const scroll = document.getElementById('scrollText')
        scroll.scrollTop = scroll.scrollHeight
      })
    } else {
      alert(data.data.msg)
    }
  })
}

onMounted(() => {
  handleImg()
})

const handleImg = async () => {
  const r = await import('../img/left.png')
  const p = await import('../img/right.png')
  const l = await import("../img/logo.png")
  robotHead.value = r.default
  peopleHead.value = p.default
  logoHead.value = l.default
}

</script>
