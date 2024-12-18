<template>
  <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3">
    <!-- All videos (including local video) -->
    <li v-for="(stream, userId) in remoteStreams" :key="userId" 
        class="col-span-1 flex flex-col divide-y divide-gray-200 rounded-lg bg-white text-center shadow">
      <div class="flex flex-1 flex-col p-8">
        <video :ref="el => setVideoRef(el, userId)" 
               :muted="userId === localUserId" 
               autoplay 
               class="w-full">
        </video>
        <h3 class="mt-6 text-sm font-medium text-gray-900">
          {{ userId === localUserId ? 'You' : `Participant ${userId}` }}
        </h3>
      </div>
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject, nextTick } from 'vue';
import { useRoute } from 'vue-router';

const socket = inject('socket');
const route = useRoute();
const meetingId = route.params.name;

const remoteStreams = ref({});
const videoElements = {};
const localUserId = ref(null);

// 存储视频元素引用
const setVideoRef = (el, userId) => {
  if (el) {
    videoElements[userId] = el;
  }
};

// 开启本地视频流
const startLocalStream = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 }
      }
    });

    // 获取本地用户ID (从socket或其他地方)
    localUserId.value = socket.id; // 或其他方式获取用户ID
    
    // 将本地流添加到remoteStreams中
    remoteStreams.value[localUserId.value] = true;
    
    // 在下一个tick更新后设置视频流
    nextTick(() => {
      if (videoElements[localUserId.value]) {
        videoElements[localUserId.value].srcObject = stream;
      }
    });

    // 每隔固定时间发送视频帧
    setInterval(() => {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      canvas.width = 640;
      canvas.height = 480;
      
      // 确保视频元素存在
      if (videoElements[localUserId.value]) {
        context.drawImage(videoElements[localUserId.value], 0, 0, canvas.width, canvas.height);
        
        // 压缩图像质量
        const frame = canvas.toDataURL('image/jpeg', 0.5);
        socket.emit('video_frame', {
          frame,
          meetingId,
        });
      }
    }, 100); // 约10fps
  } catch (err) {
    console.error("Error accessing camera:", err);
  }
};

onMounted(() => {
  startLocalStream();

  // 接收其他参与者的视频帧
  socket.on('video_frame', ({ userId, frame }) => {
    if (!remoteStreams.value[userId]) {
      remoteStreams.value[userId] = true;
    }
    
    if (videoElements[userId] && userId !== localUserId.value) {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 640;
        canvas.height = 480;
        context.drawImage(img, 0, 0);
        
        // 将canvas内容转换为视频帧
        if (!videoElements[userId].srcObject) {
          videoElements[userId].srcObject = canvas.captureStream();
        }
      };
      img.src = frame;
    }
  });
});

onUnmounted(() => {
  // 清理所有视频流
  Object.values(videoElements).forEach(element => {
    if (element && element.srcObject) {
      element.srcObject.getTracks().forEach(track => track.stop());
    }
  });
});
</script>
