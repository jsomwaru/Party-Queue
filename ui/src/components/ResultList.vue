<template>
  <template  v-for="item in results.results" :key="item.videoId">
    <a @click="addToQueue">
      <QListItem
        :title="item.title"
        :video-id="item.videoId"
        :img-link="item.thumbnails[0].url">
      </QListItem>
    </a>
  </template>
</template>

<script setup>
  import QListItem from "./QListItem.vue"
  import {defineProps} from "vue"

  const props = defineProps({
    results: Array
  })

  const addToQueue = async (event) => {
    let videoId = event.target.getAttribute("video-id")
    let req = {videoId}
    await props.results.submit(req)
  }

</script>