<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img style="cursor: pointer;" @click="goToMainPage" class="mx-auto h-10 w-auto" src="/src/assets/image.png" alt="GanLiu" />
      <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-white">Connect with your server</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6" @submit.prevent="handleLogin">
        <div>
          <label for="ip" class="block text-sm/6 font-medium text-white">IP address</label>
          <div class="mt-2">
            <input id="ip" v-model="ip" name="email"  required="" class="block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm/6" />
          </div>
        </div>
        <div>
          <div class="flex items-center justify-between">
            <label for="port" class="block text-sm/6 font-medium text-white">Port</label>
            
          </div>
          <div class="mt-2">
            <input id="port" v-model="port" name="port"  required="" class="block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm/6" />
          </div>
        </div>

        <div>
          <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500">Connect</button>
        </div>
      </form>


    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      ip: '',
      port: ''
    };
  },
  methods: {
    goToMainPage() {
      this.$router.push('/');
    },
    handleLogin() {
      
    },
    async handleLogin() {
      try {
        const response = await axios.post(`http://${this.ip}:${this.port}/connect`, {
          // 这里可以添加需要发送的数据
        });
        console.log('连接成功:', response.data);
        this.$router.push('/dashboard');
      } catch (error) {
        alert(error)
      }
    }
  }
};
</script>