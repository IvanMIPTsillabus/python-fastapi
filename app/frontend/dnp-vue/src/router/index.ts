import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Auth from '../components/Auth.vue';
import Profile from '../components/Profile.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true } // Помечаем, что для этого маршрута нужна авторизация
  },
  {
    path: '/auth',
    name: 'Auth',
    component: Auth
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token'); // Проверяем, есть ли токен
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Если маршрут требует авторизации и пользователь не авторизован, перенаправляем на страницу авторизации
    next('/auth');
  } else {
    next();
  }
});

export default router;
