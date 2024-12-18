<template>
  <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3">
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
import { ref, onMounted, onUnmounted, inject } from 'vue';
import { useRoute } from 'vue-router';

const socket = inject('socket');
const route = useRoute();
const meetingId = route.params.name;

const remoteStreams = ref({});
const videoElements = {};
const localUserId = ref(null);
let localStream = null;

// 存储视频元素引用
const setVideoRef = (el, userId) => {
  if (el) {
    videoElements[userId] = el;
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

    // 获取本地用户ID
    localUserId.value = socket.id;

    // 创建用于捕获视频帧的隐藏视频元素
    const hiddenVideo = document.createElement('video');
    hiddenVideo.srcObject = localStream;
    hiddenVideo.autoplay = true;
    hiddenVideo.style.display = 'none';
    document.body.appendChild(hiddenVideo);

    // 每隔固定时间发送视频帧
    setInterval(() => {
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
    }, 100); // 约10fps
  } catch (err) {
    console.error("Error accessing camera:", err);
  }
};

onMounted(() => {
  startLocalStream();

  // 接收所有参与者(包括自己)的视频帧
  socket.on('video_frame', ({ userId, frame }) => {
    if (!remoteStreams.value[userId]) {
      remoteStreams.value[userId] = true;
    }
    console.log(userId);
    if (videoElements[userId]) {
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
        } else {
          // 更新现有视频流
          const imageCapture = new ImageCapture(videoElements[userId].srcObject.getVideoTracks()[0]);
          imageCapture.grabFrame().then(imageBitmap => {
            context.drawImage(imageBitmap, 0, 0);
          });
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
  
  // 清理本地媒体流
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop());
  }
  
  // 移除隐藏的视频元素
  const hiddenVideo = document.querySelector('video[style="display: none;"]');
  if (hiddenVideo) {
    hiddenVideo.remove();
  }
});
</script>
