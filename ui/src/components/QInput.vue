<template>
  <div class="qinput">
  <form @submit.prevent="search">
    <label :for="id">{{ inputLabel }}</label>
    <input :type="inputType" name="song" value="" class="qinput" :id="id"/>
    <button type="submit">Submit</button>
  </form>
  </div>
</template>

<script setup>
  import { defineProps, defineExpose, ref } from 'vue';

  const results = ref([])

  let id = (Math.random() + 1).toString(36).substring(4)

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
    /* background-color: white; */
    transition: width 0.4s ease-in-out;
    border-color: whitesmoke;
  }
</style>