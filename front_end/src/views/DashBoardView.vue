<template>
    <div>
      <!-- Static sidebar for desktop -->
      <div class="hidden xl:fixed xl:inset-y-0 xl:z-50 xl:flex xl:w-72 xl:flex-col">
        <!-- Sidebar component, swap this element with another sidebar if you like -->
        <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-black/10 px-6 ring-1 ring-white/5">
          <div class="flex h-16 shrink-0 items-center">
            <img class="h-8 w-auto" src="/src/assets/image.png" alt="Your Company" />
          </div>
          <nav class="flex flex-1 flex-col">
            <ul role="list" class="flex flex-1 flex-col gap-y-7">
              <li>
                <ul role="list" class="-mx-2 space-y-1">
                  <li v-for="item in navigation" :key="item.name">
                    <a :href="item.href" :class="[item.current ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-gray-900', 'group flex gap-x-3 rounded-md p-2 text-sm/6 font-semibold']">
                      <component :is="item.icon" class="size-6 shrink-0" aria-hidden="true" />
                      {{ item.name }}
                    </a>
                  </li>
                </ul>
              </li>
              
              <li class="-mx-6 mt-auto">
                <a href="#" class="flex items-center gap-x-4 px-6 py-3 text-sm/6 font-semibold text-gray-900 hover:bg-gray-800">
                  <img class="size-8 rounded-full bg-gray-800" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" />
                  <span class="sr-only">Your profile</span>
                  <span aria-hidden="true">Tom Cook</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
  
      <div class="xl:pl-72">
        <main class="lg:pr-px">
          <header class="flex items-center justify-between border-b border-gray-500/5 px-4 py-4 sm:px-6 sm:py-6 lg:px-8">
            <h1 class="text-base/7 font-semibold text-gray-900">Meetings</h1>
            <Menu as="div" class="relative">
              <button  class="flex items-center gap-x-1 text-sm/6 font-medium text-gray-900">
                Refresh
                <ArrowPathIcon class="size-5 text-gray-500" aria-hidden="true" />
              </button>
            </Menu>
            <Menu as="div" class="relative">
              <button @click="createNewMeeting" class="flex items-center gap-x-1 text-sm/6 font-medium text-gray-900">
                New Meeting
                <PlusIcon class="size-5 text-gray-500" aria-hidden="true" />
              </button>
            </Menu>
          </header>
  
          <!-- Meeting list -->
          <ul role="list" class="divide-y divide-gray-500/5">
            <li v-for="meeting in meetings" :key="meeting.id" class="relative flex items-center space-x-4 px-4 py-4 sm:px-6 lg:px-8">
              <div class="min-w-0 flex-auto">
                <div class="flex items-center gap-x-3">
                  <div :class="[statuses[meeting.status], 'flex-none rounded-full p-1']">
                    <div class="size-2 rounded-full bg-current" />
                  </div>
                  <h2 class="min-w-0 text-sm/6 font-semibold text-gray-900">
                    <a :href="meeting.href" class="flex gap-x-2">
                      <span class="truncate">{{ meeting.hostName }}</span>
                      <span class="text-gray-400">/</span>
                      <span class="whitespace-nowrap">{{ meeting.meetingName }}</span>
                      <span class="absolute inset-0" />
                    </a>
                  </h2>
                </div>
                <div class="mt-3 flex items-center gap-x-2.5 text-xs/5 text-gray-400">
                  <p class="truncate">{{ meeting.description }}</p>
                  <svg viewBox="0 0 2 2" class="size-0.5 flex-none fill-gray-300">
                    <circle cx="1" cy="1" r="1" />
                  </svg>
                </div>
              </div>
              <ChevronRightIcon class="size-5 flex-none text-gray-400" aria-hidden="true" />
            </li>
          </ul>
        </main>
  
      </div>
    </div>
  </template>
  
  <script setup>
  import { ArrowPathIcon, PlusIcon, ServerIcon } from '@heroicons/vue/24/outline';
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import io from 'socket.io-client';
import router from '../router';
  
  const navigation = [
    { name: 'Meeting list', href: '#', icon: ServerIcon, current: true },
  ];
  
  const statuses = {
    offline: 'text-gray-500 bg-gray-100/10',
    online: 'text-green-400 bg-green-400/10',
    error: 'text-rose-400 bg-rose-400/10',
  };
  
  // 使用 ref 管理会议列表
  const meetings = ref([
    // {
    //   id: 1,
    //   href: '#',
    //   meetingName: 'work hard',
    //   hostName: 'SheepDoctor',
    //   status: 'offline',
    //   description: 'work work',
    // },
  ]);
  
  let socket;
  
  const createNewMeeting = () => {
    router.push('/new');
  };
  
  const updateMeetingsList = (newMeetings) => {
    meetings.value = [];
    meetings.value.push(...newMeetings);
    
  };
  
  onMounted(() => {
    socket = io.connect('http://localhost:5001',{'force new connection': true});
    socket.on('newMeeting', updateMeetingsList);
  });
  
  onBeforeUnmount(() => {
    if (socket) {
      socket.off('newMeeting');
      socket.disconnect();
    }
  });
  </script>