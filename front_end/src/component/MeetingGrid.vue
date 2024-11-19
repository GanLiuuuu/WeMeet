<template>
  <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3">
    <li class="col-span-1 flex flex-col divide-y divide-gray-200 rounded-lg bg-white text-center shadow">
      <div class="flex flex-1 flex-col p-8">
          <video  id="video" autoplay width="640" height="480" controls></video>
        <!-- 视频流展示 -->
        <img id="received-image" width="640" height="480">
        <h3 class="mt-6 text-sm font-medium text-gray-900">Your Camera</h3>
      </div>
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted , defineProps, inject} from 'vue';
const socket = inject('socket')

const videoElements = ref(null);
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');

const startVideoStream = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });

    // 获取视频元素并将其连接到视频流
    const videoElement = document.getElementById('video');
    videoElement.srcObject = stream;

    sendVideoStream(stream);
  } catch (err) {
    console.error("Failed to get camera video stream:", err);
  }
};

const sendVideoStream = (stream) => {
  // 设置 canvas 的大小与视频流一致
  const clonedVideoElement= document.getElementById('video');
  const videoElement = document.getElementById('video');
  canvas.width = videoElement.videoWidth || 640;  // 默认宽度 640
  canvas.height = videoElement.videoHeight || 480;  // 默认高度 480
  function sendFrameToServer() {
    if (!stream.active) return;
    
    // 将当前的视频帧绘制到 canvas 上
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    // 获取图片数据并发送给服务器
    canvas.toBlob((blob) => {
      if (socket.connected) {
        socket.emit('video_frame', blob);  // 发送视频帧到服务器
      }
    }, 'image/jpeg', 0.9);
  }

  // 使用 setInterval 每 100 毫秒抓取一次视频帧
  setInterval(sendFrameToServer, 100);
};

const receiveProcessedFrame = () => {
  if (socket) {
    socket.on('processed_frame', (frame_data) => {
      // 将接收到的图像数据转换为图像 URL
      const arrayBuffer = frame_data;
      const blob = new Blob([arrayBuffer], { type: 'image/jpeg' });
      const url = URL.createObjectURL(blob);

      // 将接收到的图像显示到页面上
      const imgElement = document.getElementById('received-image');
      imgElement.src = url;  // 更新 img 元素的 src 属性
    });
  }
};

onMounted(() => {
  receiveProcessedFrame();
  startVideoStream();  // 启动视频流
});
</script>
