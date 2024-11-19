<!--
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/forms'),
    ],
  }
  ```
-->
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
                <div class="text-sm/6 text-gray-500">Meeting <span class="text-gray-700">{{ meetingId }}</span></div>
                <div class="mt-1 text-base font-semibold text-gray-900">GAN</div>
              </h1>
            </div>
            <div class="flex items-center gap-x-4 sm:gap-x-6">
              <a href="#" class="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600">Exit</a>

            </div>
          </div>
        </div>
      </header>
  
      <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div class="mx-auto grid max-w-2xl grid-cols-1 grid-rows-1 items-start gap-x-8 gap-y-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">
 
  
          <!-- Meeting Grid -->
          <div class="-mx-4 px-4 py-8 shadow-sm ring-1 ring-gray-900/5 sm:mx-0 sm:rounded-lg sm:px-8 sm:pb-14 lg:col-span-2 lg:row-span-2 lg:row-end-2 xl:px-16 xl:pb-20 xl:pt-16">
            <div class="w-full">
                <MeetingGrid/>
            </div>

          </div>
  
          <div class="lg:col-start-3">
            <!-- Chatting area -->
            <h2 class="text-sm/6 font-semibold text-gray-900">Chat</h2>
            <ul role="list" class="mt-6 space-y-6">
              <li v-for="(message, messageIdc) in chat" :key="message.id" class="relative flex gap-x-4">
                <div :class="[messageIdc === chat.length - 1 ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
                  <div class="w-px bg-gray-200" />
                </div>
                <template v-if="message.type === 'commented'">
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
                </template>
                <template v-else>
                  <div class="relative flex size-6 flex-none items-center justify-center bg-white">
                    <CheckCircleIcon v-if="message.type === 'paid'" class="size-6 text-indigo-600" aria-hidden="true" />
                    <div v-else class="size-1.5 rounded-full bg-gray-100 ring-1 ring-gray-300" />
                  </div>
                  <p class="flex-auto py-0.5 text-xs/5 text-gray-500">
                    <span class="font-medium text-gray-900">{{ message.person.name }}</span> {{ message.type }} the invoice.
                  </p>
                  <time :datetime="message.dateTime" class="flex-none py-0.5 text-xs/5 text-gray-500">{{ message.date }}</time>
                </template>
              </li>
            </ul>
  
            <!-- New Message -->
            <div class="mt-6 flex gap-x-3">
              <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" class="size-6 flex-none rounded-full bg-gray-50" />
              <form action="#" class="relative flex-auto">
                <div class="overflow-hidden rounded-lg pb-12 shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-indigo-600">
                  <label for="comment" class="sr-only">Add your comment</label>
                  <textarea rows="2" name="comment" id="comment" class="block w-full resize-none border-0 bg-transparent py-1.5 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6" placeholder="Add your comment..." />
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
  import { ref, onMounted } from 'vue'
  import MeetingGrid from '../component/MeetingGrid.vue'
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
  import { defineProps } from 'vue';
  import io from 'socket.io-client';

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const meetingId = props.id;


  const chat = ref([])
  
let socket;
  const connectSocket = () => {
  socket = io("http://localhost:5001")  
  socket.on('connect', () => {
    console.log("Socket.IO connected")
    socket.emit('join', { meetingId })
  })
  
  socket.on('update_chat_message', (messages) => {
    alert('hi')
  console.log("Received messages:", messages)
  chat.value = []
  // Assuming messages is an array of message objects, we push them into chat array
  chat.value.push(...messages)
})
}
  onMounted(() => {
    connectSocket()
  })
  
  
  </script>