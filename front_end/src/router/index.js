import { createRouter, createWebHistory } from 'vue-router'

import ConnectView from '../views/ConnectView.vue'
import DashBoardView from '../views/DashBoardView.vue'
const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: '/',
			component: ConnectView
		},
		{
			path: '/dashboard',
			component: () => import('../views/DashBoardView.vue')
		}


	],
})

export default router