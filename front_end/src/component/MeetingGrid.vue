<template>
  <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3">
    <li class="col-span-1 flex flex-col divide-y divide-gray-200 rounded-lg bg-white text-center shadow">
      <div class="flex flex-1 flex-col p-8">
        <!-- 视频流展示 -->
        <video ref="videoElement" autoplay playsinline class="mx-auto size-64 shrink-0"></video>

        <h3 class="mt-6 text-sm font-medium text-gray-900">Your Camera</h3>
      </div>
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 引用 video 元素
const videoElement = ref(null);

// 启动视频流
const startVideoStream = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    videoElement.value.srcObject = stream;
    sendVideoStream(stream);
  } catch (err) {
    console.error("获取摄像头视频流失败:", err);
  }
}

// 通过 WebSocket 发送视频流
const sendVideoStream = (stream) => {
  const videoTrack = stream.getVideoTracks()[0];
  const mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.ondataavailable = (event) => {
    console.log("视频数据:", event.data);
    // 如果需要的话，发送数据到 WebSocket
  };

  mediaRecorder.start(100); // 每100ms发送一次数据
}

// 组件挂载时启动视频流
onMounted(() => {
  startVideoStream();
});
</script>

<style scoped>
/* 自定义样式 */
</style>
