<template>
  <template v-if="username_set === false">
    <div class="username-input">
      <form @submit.prevent="setUsername">
        <label for="username">Username</label>
        <input type="text" name="song" :value="username" class="username-input" id="username"/>
        <button type="submit">Search</button>
      </form>
    </div>
  </template>
  <template v-else>
    <span>{{ username }}</span>
  </template>
</template>

<script setup>
  import { defineExpose, ref } from 'vue';
  
  let username = ref("")
  let username_set = ref(false)
  
  defineExpose([username]);

  (function checkUserName() {
    fetch("/whomai")
    .then((res) => {res.json()})
    .then((res) => {
      if(res.username.length > 0) {
        username.value = res.username
        username_set.value = true
      }
    })
  })();

  function setUsername(event) {
    let formData = new FormData(event.target)
    fetch("/setuser",{
      method: "post",
      body: formData
    }).then((res) => {
      if (res.ok)
        username_set.value = true;
    })
  }

</script>

<style scoped>

  .username-input { 
    float: right;
  }

</style>