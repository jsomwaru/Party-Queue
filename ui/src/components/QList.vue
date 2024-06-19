<script setup>
  import QListItem from './QListItem.vue';
  import { defineProps, ref } from 'vue';

  defineProps({
    role: String,
  })

  var queue = ref([])

  let qinfo_url = location.port != '' ?  `${window.location.hostname}:${location.port}` : `${window.location.hostname}`
  const socket = new WebSocket(`ws://${qinfo_url}/qinfo`)

  socket.addEventListener("open", () => {
    console.log("---Connected to Queue---")
  })

  socket.addEventListener("message", (event) => {
    let qdata = JSON.parse(event.data)
    queue.value = qdata
  })

  setInterval((socket) => {socket.send("inquire")}, 5000, socket)

</script>

<template>

  <template v-for="item in queue" :key="item.videoId">
    <QListItem 
      :title="item.title"
      :requested_by="item.requestor"
      :video-id="item.videoId"
      :img-link="item.thumbnails[0].url"
      :timing-info="item.pos">
    </QListItem>
  </template>

</template>
