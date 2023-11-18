<template>
  <div class="item">
    <img class="block" src={{ img_link }} width="50px" height="50px">
    <p class="block">{{ title }}</p>
    <p v-if="requested_by">{{ requested_by }}</p>
    <p v-if="timing_info" id="timing-info">{{ timing_info }}</p>
  </div>
</template>

<script>
  export default {
    name: 'QListItem',
    props: {
      title: String,
      img_link: String,
      requested_by: String,
      video_id: String,
      timing_info: String
    },
  }
</script>

<style>
  .block {
    display: inline-block;
  }

  .item {
    padding: 10px;
  }
</style>
