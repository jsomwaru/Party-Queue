<template>
  <template  v-for="item in results.results" :key="item.videoId">
    <a>
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
  defineProps({
    results: Array
  })
</script>