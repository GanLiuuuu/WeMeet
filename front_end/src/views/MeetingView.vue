<template>
    <main>
      <header class="relative isolate pt-">
        <div class="absolute inset-0 -z-10 overflow-hidden" aria-hidden="true">
          <div class="absolute left-16 top-full -mt-16 transform-gpu opacity-50 blur-3xl xl:left-1/2 xl:-ml-80">
            <div class="aspect-[1154/678] w-[72.125rem] bg-gradient-to-br from-[#FF80B5] to-[#9089FC]" style="clip-path: polygon(100% 38.5%, 82.6% 100%, 60.2% 37.7%, 52.4% 32.1%, 47.5% 41.8%, 45.2% 65.6%, 27.5% 23.4%, 0.1% 35.3%, 17.9% 0%, 27.7% 23.4%, 76.2% 2.5%, 74.2% 56%, 100% 38.5%)" />
          </div>
          <div class="absolute inset-x-0 bottom-0 h-px bg-gray-900/5" />
        </div>
  
        <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
          <div class="mx-auto flex max-w-2xl items-center justify-between gap-x-8 lg:mx-0 lg:max-w-none">
            <div class="flex items-center gap-x-6">
              <h1>
                <div class="text-sm/6 text-gray-500">Meeting <span class="text-gray-700"></span></div>
                <div class="mt-1 text-base font-semibold text-gray-900">{{ meetingName }}</div>
              </h1>
            </div>
            <div class="flex items-center gap-x-4 sm:gap-x-6">
              <button @click="handleExit" class="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600">Exit</button>
              <button  @click="handleCancel" class="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600">Cancel</button>
            </div>
          </div>
        </div>
      </header>
  
      <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div class="mx-auto grid max-w-2xl grid-cols-1 grid-rows-1 items-start gap-x-8 gap-y-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">
 
  
          <!-- Meeting Grid -->
          <div v-if="isSocketReady" class="-mx-4 px-4 py-8 shadow-sm ring-1 ring-gray-900/5 sm:mx-0 sm:rounded-lg sm:px-8 sm:pb-14 lg:col-span-2 lg:row-span-2 lg:row-end-2 xl:px-16 xl:pb-20 xl:pt-16">
            <div class="w-full">
                <MeetingGrid/>
            </div>

          </div>
  
          <div class="lg:col-start-3">
            <!-- Chatting area -->
            <div class="chat-container">
              <h2 class="text-sm/6 font-semibold text-gray-900">
                Chat ({{ chat.length }} messages)
              </h2>
              <ul role="list" class="mt-6 space-y-6">
                <li v-for="message in chat" :key="message.id" class="relative flex gap-x-4">
                  <pre v-if="false">{{ JSON.stringify(message, null, 2) }}</pre>
                  <img :src="message.person.imageUrl" alt="" class="relative mt-3 size-6 flex-none rounded-full bg-gray-50" />
                  <div class="flex-auto rounded-md p-3 ring-1 ring-inset ring-gray-200">
                    <div class="flex justify-between gap-x-4">
                      <div class="py-0.5 text-xs/5 text-gray-500">
                        <span class="font-medium text-gray-900">{{ message.person.name }}</span> commented
                      </div>
                      <time :datetime="message.dateTime" class="flex-none py-0.5 text-xs/5 text-gray-500">{{ message.date }}</time>
                    </div>
                    <p class="text-sm/6 text-gray-500">{{ message.comment }}</p>
                  </div>
                </li>
              </ul>
            </div>
  
            <!-- New Message -->
            <div class="mt-6 flex gap-x-3">
              <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" class="size-6 flex-none rounded-full bg-gray-50" />
              <form action="#" class="relative flex-auto" @submit.prevent="handleSubmit">
                <div class="overflow-hidden rounded-lg pb-12 shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-indigo-600">
                  <label for="comment" class="sr-only">Add your comment</label>
                  <textarea
                    v-model="newComment"
                    rows="2"
                    name="newComment"
                    id="newComment"
                    class="block w-full resize-none border-0 bg-transparent py-1.5 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6"
                    placeholder="Add your comment..."
                  />                
                </div>
  
                <div class="absolute inset-x-0 bottom-0 flex justify-between py-2 pl-3 pr-2">
                  
                  <button type="submit" class="rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">Comment</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useRouter, onBeforeRouteLeave } from 'vue-router'
  import {
    Dialog,
    DialogPanel,
    Listbox,
    ListboxButton,
    ListboxLabel,
    ListboxOption,
    ListboxOptions,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
  } from '@headlessui/vue'
  import {
    Bars3Icon,
    CalendarDaysIcon,
    CreditCardIcon,
    EllipsisVerticalIcon,
    FaceFrownIcon,
    FaceSmileIcon,
    FireIcon,
    HandThumbUpIcon,
    HeartIcon,
    PaperClipIcon,
    UserCircleIcon,
    XMarkIcon as XMarkIconMini,
  } from '@heroicons/vue/20/solid'
  import { BellIcon, XMarkIcon as XMarkIconOutline } from '@heroicons/vue/24/outline'
  import { CheckCircleIcon } from '@heroicons/vue/24/solid'
  import { defineProps, provide } from 'vue';
  import io from 'socket.io-client';
  import MeetingGrid from '../component/MeetingGrid.vue';
  import router from '../router';
const newComment = ref('')
const props = defineProps({
  name: {
    type: String,
    required: true,
  },
});

const meetingName = props.name;


  const chat = ref([])
  
  let socket = null;
  const isSocketReady = ref(false); 

  // 添加获取历史记录的函数
  const requestChatHistory = () => {
    console.log("Requesting chat history for meeting:", meetingName);
    socket.emit('join', { meetingName });
  }

  const connectSocket = () => {
    console.log("Initializing socket connection...");
    socket = io("http://localhost:5001");  // 使用默认配置

    socket.on('connect', () => {
      console.log("Socket.IO connected");
      isSocketReady.value = true;
      requestChatHistory();
    });

    socket.on('connect_error', (error) => {
      console.error("Socket connection error:", error);
    });

    socket.on('connect_timeout', () => {
      console.error("Socket connection timeout");
    });
  }

  const handleCancel = () => {
    if (socket) {
      socket.emit('cancel', { meetingName });
    }
    router.push('/');
  }
  const handleExit = () => {
    if (socket) {
      socket.emit('exit', { meetingName });
    }
    router.push('/');
  }
  onMounted(() => {
    console.log("Component mounted, connecting socket...");
    connectSocket();
    provide('socket', socket);

    socket.on('update_chat_message', function(data) {
      console.log("Socket received update_chat_message event");
      console.log("Raw data received:", data);
      
      try {
        if (!data || !data.message) {
          console.warn("Received empty data or message");
          return;
        }

        let messages = [];
        if (Array.isArray(data.message)) {
          console.log("Processing array message:", data.message);
          messages = data.message;
        } else if (typeof data.message === 'object' && data.message !== null) {
          console.log("Processing object message:", data.message);
          messages = Object.values(data.message);
        } else {
          console.warn("Invalid message format:", data.message);
          return;
        }

        // 确保所有消息都有必要的字段
        messages = messages.filter(msg => {
          const isValid = msg && msg.id && msg.person && msg.comment && msg.dateTime;
          if (!isValid) {
            console.warn("Filtered out invalid message:", msg);
          }
          return isValid;
        });

        const sortedMessages = messages.sort((a, b) => 
          new Date(a.dateTime) - new Date(b.dateTime)
        );

        console.log("Final sorted messages:", sortedMessages);
        chat.value = sortedMessages;
      } catch (error) {
        console.error("Error processing chat update:", error);
        console.error("Problematic data:", data);
      }
    });

    socket.on('disconnect', () => {
      console.log('Socket disconnected');
      isSocketReady.value = false;
    });
  });

  // 处理组件销毁时的清理
  onBeforeRouteLeave((to, from) => {
    if (socket) {
      socket.disconnect();
    }
  });

const handleSubmit = () => {
  if(newComment.value.trim() !== '') {
    const currentDateTime = new Date();
    const message = {
      id: chat.value.length + 1,
      type: 'commented',
      person: {
        name: 'Gan',
        imageUrl: 'https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
      },
      comment: newComment.value.trim(),
      date: currentDateTime.toLocaleDateString(),
      dateTime: currentDateTime.toISOString(),
      meeting_id: meetingName
    };
    console.log("Sending message:", message);
    socket.emit('createMessage', { message, meetingName });
    newComment.value = '';
  }
};

// 添加 watch 来监控聊天记录的变化
watch(chat, (newVal, oldVal) => {
  console.log("Chat ref changed:");
  console.log("Old value:", oldVal);
  console.log("New value:", newVal);
}, { deep: true });

  
</script>

<style scoped>
.chat-container {
  max-height: 500px;
  overflow-y: auto;
}
</style>


