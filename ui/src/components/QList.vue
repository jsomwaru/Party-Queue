<script setup>
  import QListItem from './QListItem.vue';
  import { defineProps, ref } from 'vue';

  defineProps({
    role: String,
  })

  // eslint-disable-next-line no-unused-vars
  var queue = ref([])

  let qinfo_url = location.port != '' ?  `${window.location.hostname}:${location.port}` : `${window.location.hostname}`
  const socket = new WebSocket(`ws://${qinfo_url}/qinfo`)

  socket.addEventListener("open", () => {
    console.log("socket open")
  })

  socket.addEventListener("message", (event) => {
    let qdata = JSON.parse(event.data)
    console.log(qdata)
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
