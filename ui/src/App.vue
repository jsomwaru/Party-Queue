<template>
  <ToggleButton/>
  <UsernameInput/>
  <QList role="queue"></QList>
  <QInput input-label="Song:" input-type="text" ref="searchResults" />
  <ResultList :results="searchResults" ></ResultList>
</template>

<script setup>
  import QList from './components/QList.vue';
  import QInput from './components/QInput.vue';
  import ResultList from "./components/ResultList.vue"
  import ToggleButton from "./components/ToggleButton.vue"
  import UsernameInput from './components/UsernameInput.vue';

  import { ref } from 'vue';

  const searchResults = ref([])
</script>

<style>
  body {
    font-family: monospace;
    font-size: large;
    background-color: #b2e0df;
  }
  #app {
    font-family: monospace;
    font-size: large;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    /* text-align: center; */
    color: #2c3e50;
    /* margin-top: 60px; */
  }
</style>
