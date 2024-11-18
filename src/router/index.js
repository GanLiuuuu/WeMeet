import { createRouter, createWebHistory } from 'vue-router'

import ConnectView from '../views/ConnectView.vue'
const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: '/',
			component: ConnectView
		}

	],
})

export default router