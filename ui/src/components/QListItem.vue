<template>
  <div class="block" :video-id="videoId">
    <img  :src="imgLink" width="75" height="75" :video-id="videoId">
  </div>
    <div class="details">
      <span class="item" :video-id="videoId">{{ title }}</span>
      <span class="item" :video-id="videoId">{{ artist }}</span>
      <div class="break"></div>
      <span class="item" v-if="timingInfo" id="timing-info" :video-id="videoId">{{ timingInfo }}</span>
      <div  v-if="requestedBy" class="break"></div>
      <span v-if="requestedBy" :video-id="videoId">{{ requestedBy }}</span>
    </div>
</template>

<script>
  export default {
    name: 'QListItem',
    props: {
      title: String,
      artist: String,
      imgLink: String,
      requestedBy: String,
      videoId: String,
      timingInfo: String
    },
  }
</script>

<style>
  .block {
    display: block;
    padding-left: 10px;
  }

  .break {
    flex-basis: 100%;
    height: 0;
  }

  .item {
    padding: 10px;
  }
</style>
