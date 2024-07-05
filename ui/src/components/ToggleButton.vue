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