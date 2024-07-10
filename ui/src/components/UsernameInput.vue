<template>
  <template v-if="username_set === false">
    <div class="username-input">
      <form @submit.prevent="setUsername">
        <label for="username">Username: </label>
        <input type="text" name="username" value="" class="username-input" id="username"/>
        <button type="submit">Set Username</button>
      </form>
    </div>
  </template>
  <template v-else>
    <span class="username-input">{{ username }}</span>
  </template>
</template>

<script setup>
  import { defineExpose, ref } from 'vue';
  
  let username = ref("")
  let username_set = ref(false)
  
  defineExpose([username]);

  (function checkUserName() {
    fetch("/whoami")
    .then((res) => { return res.json() })
    .then((res) => {
      if(res.username.length > 0) {
        username.value = res.username
        username_set.value = true
      }
    })
    .catch(e => console.error(e))
  })();

  function setUsername(event) {
    let formData = new FormData(event.target)
    fetch("/setuser",{
      method: "post",
      body: formData
    }).then((res) => {
      if (res.ok) {
        username_set.value = true;
        return res.json()
      }
    }).then((res) => {username.value = res.username})
  }

</script>

<style scoped>

  .username-input { 
    float: right;
  }

</style>