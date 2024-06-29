<template>
  <div class="qinput">
  <form @submit.prevent="search">
    <p>{{ inputLabel }}</p>
    <input :type="inputType" name="song" value="" class="qinput"/>
    <button type="submit">Submit</button>
  </form>
  </div>
</template>

<script setup>
  import { defineProps, defineExpose, ref } from 'vue';

  const results = ref([])

  const ERROR_MESG = {
    error: 1, 
    message: "Failed gettings song information"
  }

  defineProps({
    inputLabel: String,
    inputType: String,
  })

  defineExpose({
    results,
    submit
  })

  async function search(event) {
    let form = new FormData(event.target)
    var res = await fetch(window.origin, {
      method: "post",
      body: form
    })
    if (res.ok)
      results.value = await res.json()
    else {
      results.value  = ERROR_MESG
    }
  }

  async function submit(songreq) {
    var res = await fetch(`${window.origin}/add`, { 
      method: "post",
      body: JSON.stringify(songreq)
    })
    if (res.ok)
      return 
  }

</script>

<style>
  .qinput {
    width: 80%;
    margin: 10px auto;
  };

</style>