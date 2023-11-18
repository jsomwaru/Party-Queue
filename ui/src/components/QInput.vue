<template>
  <form>
    <p>{{ inputLabel }}</p>
    <input  :type="inputType"/>
    <button type="submit">Submit</button>
  </form>
</template>

<script setup>
  import {  defineProps } from 'vue';
  // let inputLabel = ref(null);
  // let inputType = ref(null);

  defineProps({
    inputLabel: String,
    inputType: String,
  })
</script>