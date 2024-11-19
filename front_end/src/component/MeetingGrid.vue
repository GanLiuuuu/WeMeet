<template>
  <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3">
    <li v-for="person in people" :key="person.name" class="col-span-1 flex flex-col divide-y divide-gray-200 rounded-lg bg-white text-center shadow">
      <div class="flex flex-1 flex-col p-8">
        <!-- 视频流展示 -->
        <video ref="videoElements" :ref="person.name" autoplay playsinline class="mx-auto size-64 shrink-0"></video>
        <h3 class="mt-6 text-sm font-medium text-gray-900">{{ person.name }}</h3>
      </div>
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted , defineProps, inject} from 'vue';
const socket = inject('socket')

const videoElements = ref({});

const people = ref([
])
const startVideoStream = async (name) => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoElements.value[name].srcObject = stream; // Assign the stream to the corresponding video element
    sendVideoStream(stream);
    registerUser(name); // Register user with the WebSocket
  } catch (err) {
    console.error("Failed to get camera video stream:", err);
  }
};

const sendVideoStream = (stream) => {
  const mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.ondataavailable = (event) => {
    console.log("Video data:", event.data);
    // Emit the video data to the server
    socket.emit('video_data', { data: event.data });
  };

  mediaRecorder.start(100);
};
const registerUser = (name) => {
  socket.emit('register_user', { name }); 
};

const receiveUserList = () => {
  if(socket){
    socket.on('user_list', (users) => {
    people.value = Object.values(users).map(user => ({
      name: user.name,
      videoStream: null 
    }));
  });
  }
  
};
onMounted(() => {
  receiveUserList();
  startVideoStream('Your Name'); 
});
</script>
