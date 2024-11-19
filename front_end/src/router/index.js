import { createRouter, createWebHistory } from 'vue-router'

import ConnectView from '../views/ConnectView.vue'
import DashBoardView from '../views/DashBoardView.vue'
import MeetingView from '../views/MeetingView.vue'
import NewMeetingView from '../views/NewMeetingView.vue'
const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: '/',
			component: DashBoardView

		},
		{
			path: '/dashboard',
			component: () => import('../views/DashBoardView.vue')
		},
		{
			path: '/meeting',
			component: MeetingView
		},
		{
			path: '/new',
			component: NewMeetingView
		}


	],
})

export default router