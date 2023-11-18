<script setup>
  import QListItem from './QListItem.vue';
  import { defineProps, defineExpose } from 'vue';

  import {ref} from 'vue';
  var data = ref([]); 

  defineProps({
    role: String
  })

  defineExpose({
    data
  })
</script>

<template>
  <div v-if="role==='queue'" class="qtable">
    <template v-for="item in data" :key="item.videoId">
      <QListItem :title="item.title" 
      :img_link="item.thumbnails[0].url"
      :requested_by="item.requestor"
      :video_id="item.videoId"
      :timing_info="item.pos"></QListItem>
    </template>
  </div>
  <div v-else-if="role==='results'" class="qtable">
    <template  v-for="item in data" :key="item.videoId">
      <a videoId={{ item.videoId }}>
        <QListItem :title="item.title" 
        :img_link="item.thumbnails[0].url"
        :video_id="item.videoId">
        </QListItem>
      </a>
    </template>
  </div>
</template>
