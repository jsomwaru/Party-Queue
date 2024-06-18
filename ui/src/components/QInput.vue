<template>
  <form @submit.prevent="search">
    <p>{{ inputLabel }}</p>
    <input :type="inputType" name="song" value="" />
    <button type="submit">Submit</button>
  </form>
</template>

<script setup>
  import { defineProps, defineExpose, ref } from 'vue';

  const results = ref(null)

  const ERROR_MESG = {
    error: 1, 
    message: "Failed gettings song information"
  }

  defineProps({
    inputLabel: String,
    inputType: String,
  })

  defineExpose([results])

  async function search(event) {
    console.log(event.target)
    let form = new FormData(event.target)
    var res = await fetch(window.origin, {
      method: "post",
      body: form
    })
    if (res.ok)
      results.value = res.json()
    else {
      results.value  = ERROR_MESG
    }
  }

</script>