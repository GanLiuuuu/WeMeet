<template>
    <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3">
      <li v-for="person in people" :key="person.email" class="col-span-1 flex flex-col divide-y divide-gray-200 rounded-lg bg-white text-center shadow">
        <div class="flex flex-1 flex-col p-8">
          <img class="mx-auto size-64 shrink-0" :src="person.imageUrl" alt="" />
          <h3 class="mt-6 text-sm font-medium text-gray-900">{{ person.name }}</h3>
          <dl class="mt-1 flex grow flex-col justify-between">
            
          </dl>
        </div>
      </li>
    </ul>
  </template>
  
  <script setup>
  import { EnvelopeIcon, PhoneIcon } from '@heroicons/vue/20/solid'
  
  const people = [
    {
      name: 'Jane Cooper',
      imageUrl:
        'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=256&h=256&q=60',
    },
   

    // More people...
  ]
  </script>