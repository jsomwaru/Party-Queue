<template>
  <button @click="togglePlaying">{{ play_status }}</button>
</template> 

<script setup>
  import { ref } from 'vue';

  const play_status = ref("Pause")
  function togglePlaying(event) {
    event.preventDefault();
    fetch(`${window.origin}/toggle`, {
      method: "get"
    }).then((res) => {
      if (res.ok)
        res.text().then((text) => {
          play_status.value = text
        })
    })
  }
</script>

<style scoped>

  button {
    float: left;
    background-color: whitesmoke;
    border: none;
    color: black;
    padding: 30px 32px;
    text-align: center;
    text-decoration: none;
    /* display: inline-block; */
    font-size: 16px;
  }
</style>