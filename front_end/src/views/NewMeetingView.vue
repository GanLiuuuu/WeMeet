<template>
  <div style="padding: 40px;">
    <form @submit.prevent="handleSubmit">
      <div class="space-y-12">
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base/7 font-semibold text-gray-900">New Meeting</h2>
          <p class="mt-1 text-sm/6 text-gray-600">This information will be displayed publicly so be careful what you share.</p>
  
          <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
            <div class="sm:col-span-4">
              <label for="meetingName" class="block text-sm/6 font-medium text-gray-900">Meeting Name</label>
              <div class="mt-2">
                <div class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                  <input type="text" v-model="meetingName" name="meetingName" id="meetingName" autocomplete="off" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6" placeholder="meeting name" />
                </div>
              </div>
            </div>
            <div class="sm:col-span-4">
              <label for="hostName" class="block text-sm/6 font-medium text-gray-900">Host Name</label>
              <div class="mt-2">
                <div class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                  <input type="text" v-model="hostName" name="hostName" id="hostName" autocomplete="off" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6" placeholder="John Snow" />
                </div>
              </div>
            </div>
  
            <div class="col-span-full">
              <label for="about" class="block text-sm/6 font-medium text-gray-900">About</label>
              <div class="mt-2">
                <textarea id="about" v-model="about" name="about" rows="3" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"></textarea>
              </div>
              <p class="mt-3 text-sm/6 text-gray-600">Write a few sentences about your meeting.</p>
            </div>
          </div>
        </div>
      </div>
  
      <div class="mt-6 flex items-center justify-end gap-x-6">
        <button type="button" class="text-sm/6 font-semibold text-gray-900">Cancel</button>
        <button type="submit" class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Create</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { io } from 'socket.io-client';

const router = useRouter();
const meetingName = ref('');
const hostName = ref('');
const about = ref('');
let socket;

onMounted(() => {
  socket = io.connect('http://localhost:5001',{'force new connection': true});
});

onBeforeUnmount(() => {
  if (socket) {
    socket.disconnect();
  }
});

const handleSubmit = () => {
  const newMeeting = {
    href: '#',
    meetingName: meetingName.value,
    hostName: hostName.value,
    status: 'online',
    description: about.value,
  };

  socket.emit('createMeeting', newMeeting);
  router.push(`/meeting/${meetingName.value}`);
};
</script>