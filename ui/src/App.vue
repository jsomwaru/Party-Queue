<template>
  <QInput input-label="Song:" input-type="text"/>
  <QInput input-label="Username:" input-type="text"/>
  <QList role="results"></Qlist>
  <QList role="queue"></QList>
</template>

<script setup>
import QList from './components/QList.vue';
import QInput from './components/QInput.vue';
// import {ref} from 'vue';
// let queue = ref(null)
// let results = ref(null)

const socket = new WebSocket(`ws://${window.location.hostname}/qinfo`)

socket.addEventListener("open", () => {
  console.log("socket open")
})

</script>

<style>
body {
  font-family: monospace;
  font-size: large;
}
#app {
  font-family: monospace;
  font-size: large;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  margin-top: 60px;
}
</style>
