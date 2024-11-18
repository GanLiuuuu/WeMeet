import { createRouter, createWebHistory } from 'vue-router'

import ConnectView from '../views/ConnectView.vue'
import DashBoardView from '../views/DashBoardView.vue'
import MeetingView from '../views/MeetingView.vue'
const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: '/',
			component: MeetingView
		},
		{
			path: '/dashboard',
			component: () => import('../views/DashBoardView.vue')
		},
		{
			path: '/meeting',
			component: MeetingView
		}


	],
})

export default router