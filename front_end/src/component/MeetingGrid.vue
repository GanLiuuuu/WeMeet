<template>
  <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3">
    <li class="col-span-1 flex flex-col divide-y divide-gray-200 rounded-lg bg-white text-center shadow">
      <div class="flex flex-1 flex-col p-8">
          <video  id="video" autoplay width="640" height="480" controls></video>
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
    const videoElement = document.getElementById('video');
    videoElement.srcObject = stream;

    sendVideoStream(stream);
  } catch (err) {
    console.error("Failed to get camera video stream:", err);
  }
};

const sendVideoStream = (stream) => {
  const clonedVideoElement= document.getElementById('video');
  const videoElement = document.getElementById('video');
  canvas.width = videoElement.videoWidth || 640;
  canvas.height = videoElement.videoHeight || 480;  
  function sendFrameToServer() {
    if (!stream.active) return;
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      if (socket.connected) {
        socket.emit('video_frame', blob); 
      }
    }, 'image/jpeg', 0.9);
  }
  setInterval(sendFrameToServer, 100);
};
const receiveProcessedFrame = () => {
  if (socket) {
    socket.on('processed_frame', (frame_data) => {
      const arrayBuffer = frame_data;
      const blob = new Blob([arrayBuffer], { type: 'image/jpeg' });
      const url = URL.createObjectURL(blob);
      const imgElement = document.getElementById('received-image');
      imgElement.src = url;  
    });
  }
};
onMounted(() => {
  receiveProcessedFrame();
  startVideoStream(); 
});
</script>
