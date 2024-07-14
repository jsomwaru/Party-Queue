<template>
  <div class="wrapper">
    <div class="block" :video-id="videoId">
      <img  :src="imgLink" width="75" height="75" :video-id="videoId">
    </div>
    <div class="details">
      <span class="item" :video-id="videoId">{{ title }}</span>
      <span class="item" :video-id="videoId">By {{ artist }}</span>
      <div class="break"></div>
      <span class="item" v-if="timingInfo" id="timing-info" :video-id="videoId">{{ timingInfo }}</span>
      <div  v-if="requestedBy" class="break"></div>
      <label v-if="requestedBy" for="requestor">Requested By: </label>
      <span v-if="requestedBy" :video-id="videoId" name="requestor">{{ requestedBy }}</span>
    </div>
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
  
  .wrapper {
    display: flex;
  }

  .break {
    flex-basis: 100%;
    height: 0;
  }

  .item {
    padding: 10px;
  }
</style>
