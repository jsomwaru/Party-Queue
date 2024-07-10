<script setup>
  import QListItem from './QListItem.vue';
  import { defineProps, ref } from 'vue';

  defineProps({
    role: String,
  });

function createSocket() {
    let qinfo_url = location.port != '' ?  `${window.location.hostname}:${location.port}` : `${window.location.hostname}`
    return new WebSocket(`ws://${qinfo_url}/qinfo`)
  }

  var queue = ref([]);
  var retryInterval = null;
  let socket = null;

  (function newQueueConnection(socket) {  

    socket = createSocket()
    socket.addEventListener("open", () => {
      if (retryInterval){ 
        clearInterval(retryInterval)
      }
      console.log("---Connected to Queue---")
    })

    socket.addEventListener("message", (event) => {
      let qdata = JSON.parse(event.data)
      queue.value = qdata
    })

    // socket.onclose = () => {
    //   retryInterval = setInterval(newQueueConnection, 5000, socket)
    // }

    socket.onerror = function(err) {
      console.error('Socket encountered error: ', err.message, 'Closing socket');
      socket.close();
    };

    setInterval((socket) => {socket.send("inquire")}, 5000, socket)
  })(socket);

</script>

<template>
  <div class="qlist">
    <template v-for="item in queue" :key="item.videoId">
      <QListItem 
        :title="item.title"
        :artist="item.artists[0].name"
        :requested_by="item.requestor"
        :video-id="item.videoId"
        :img-link="item.thumbnails[0].url"
        :timing-info="item.pos">
      </QListItem>
    </template>
  </div>
</template>

<style scoped>
  .qlist {
    display: flex;
    overflow-x: auto;
    max-width: 100%;
    /* margin-top: 60px; */
    /* flex-wrap: wrap; */
  }
</style>