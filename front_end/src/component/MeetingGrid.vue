<template>
  <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3">
    <li v-for="(stream, userId) in remoteStreams" :key="userId" 
        class="col-span-1 flex flex-col divide-y divide-gray-200 rounded-lg bg-white text-center shadow">
      <div class="flex flex-1 flex-col p-8">
        <div class="relative w-full" style="padding-top: 75%">
          <img :src="stream.currentFrame" 
               class="absolute inset-0 w-full h-full object-cover"
               :class="{'opacity-100': !stream.loading, 'opacity-0': stream.loading}"
               style="transition: opacity 0.1s ease-in-out">
          <img :src="stream.nextFrame" 
               class="absolute inset-0 w-full h-full object-cover"
               :class="{'opacity-100': stream.loading, 'opacity-0': !stream.loading}"
               @load="handleImageLoad(userId)"
               style="transition: opacity 0.1s ease-in-out">
        </div>
        <h3 class="mt-6 text-sm font-medium text-gray-900">
          {{ userId === localUserId ? 'You' : `Participant ${userId}` }}
        </h3>
      </div>
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject } from 'vue';
import { useRoute } from 'vue-router';

const socket = inject('socket');
const route = useRoute();
const meetingId = route.params.name;

const remoteStreams = ref({});
const localUserId = ref(null);

// 处理图片加载成功
const handleImageLoad = (userId) => {
  console.log(`[MeetingGrid] Image loaded for user ${userId}`);
  if (remoteStreams.value[userId]) {
    const stream = remoteStreams.value[userId];
    stream.currentFrame = stream.nextFrame;
    stream.loading = false;
    console.log(`[MeetingGrid] Frame updated for user ${userId}`);
  }
};

onMounted(() => {
  console.log('[MeetingGrid] Component mounted');
  localUserId.value = socket.id;
  console.log(`[MeetingGrid] Local user ID: ${localUserId.value}`);

  socket.on('video_frame', ({ userId, frame }) => {
    console.log(`[MeetingGrid] Received video frame from user ${userId}`);
    if (!remoteStreams.value[userId]) {
      console.log(`[MeetingGrid] Creating new stream for user ${userId}`);
      remoteStreams.value[userId] = {
        currentFrame: frame,
        nextFrame: frame,
        loading: false
      };
    } else {
      console.log(`[MeetingGrid] Updating existing stream for user ${userId}`);
      const stream = remoteStreams.value[userId];
      stream.nextFrame = frame;
      stream.loading = true;
    }
  });
});

onUnmounted(() => {
  console.log('[MeetingGrid] Component unmounting');
  socket.off('video_frame');
});
</script>

<style scoped>
.opacity-0 {
  opacity: 0;
}
.opacity-100 {
  opacity: 1;
}

.object-cover {
  object-fit: cover;
}

.inset-0 {
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}
</style>
