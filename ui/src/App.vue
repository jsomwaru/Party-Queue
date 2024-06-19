<template>
  <QInput input-label="Song:" input-type="text" ref="searchResults" />
  <QInput input-label="Username:" input-type="text"/>
  <ResultList :results="searchResults" ></ResultList>
  <QList role="queue"></QList>
</template>

<script setup>
  import QList from './components/QList.vue';
  import QInput from './components/QInput.vue';
  import ResultList from "./components/ResultList.vue"

  import { ref } from 'vue';

  const searchResults = ref([])

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
