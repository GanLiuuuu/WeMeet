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
let localStream = null;

// 处理图片加载成功
const handleImageLoad = (userId) => {
  if (remoteStreams.value[userId]) {
    // 图片加载完成后，交换当前帧和下一帧
    const stream = remoteStreams.value[userId];
    stream.currentFrame = stream.nextFrame;
    stream.loading = false;
  }
};

// 开启本地视频流并发送
const startLocalStream = async () => {
  try {
    localStream = await navigator.mediaDevices.getUserMedia({ 
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 }
      }
    });

    localUserId.value = socket.id;

    const hiddenVideo = document.createElement('video');
    hiddenVideo.srcObject = localStream;
    hiddenVideo.autoplay = true;
    hiddenVideo.style.display = 'none';
    document.body.appendChild(hiddenVideo);

    hiddenVideo.onloadedmetadata = () => {
      setInterval(() => {
        try {
          const canvas = document.createElement('canvas');
          const context = canvas.getContext('2d');
          canvas.width = 640;
          canvas.height = 480;
          
          context.drawImage(hiddenVideo, 0, 0, canvas.width, canvas.height);
          
          const frame = canvas.toDataURL('image/jpeg', 0.5);
          socket.emit('video_frame', {
            frame,
            meeting: meetingId,
          });
        } catch (err) {
          console.error('Error creating frame:', err);
        }
      }, 50); // 20fps
    };
  } catch (err) {
    console.error("Error accessing camera:", err);
  }
};

onMounted(() => {
  startLocalStream();

  socket.on('video_frame', ({ userId, frame }) => {
    if (!remoteStreams.value[userId]) {
      // 初始化新的流
      remoteStreams.value[userId] = {
        currentFrame: frame.frame,
        nextFrame: frame.frame,
        loading: false
      };
    } else {
      // 更新下一帧
      const stream = remoteStreams.value[userId];
      stream.nextFrame = frame.frame;
      stream.loading = true;
    }
  });
});

onUnmounted(() => {
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop());
  }
  
  const hiddenVideo = document.querySelector('video[style="display: none;"]');
  if (hiddenVideo) {
    hiddenVideo.remove();
  }
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
