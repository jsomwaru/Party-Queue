<template>
  <div class="item" :video-id="videoId">
    <img class="block" :src="imgLink" width="50" height="50" :video-id="videoId">
    <p class="block" :video-id="videoId">{{ title }}</p>
    <p class="block" v-if="requestedBy" :video-id="videoId">{{ requestedBy }}</p>
    <p class="block" v-if="timingInfo" id="timing-info" :video-id="videoId">{{ timingInfo }}</p>
  </div>
</template>

<script>
  export default {
    name: 'QListItem',
    props: {
      title: String,
      imgLink: String,
      requestedBy: String,
      videoId: String,
      timingInfo: String
    },
  }
</script>

<style>
  .block {
    display: inline-block;
    padding-left: 10px;
  }

  .item {
    padding: 10px;
  }
</style>
