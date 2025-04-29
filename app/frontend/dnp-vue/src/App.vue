<template>
  <router-view />
</template>

<script>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();

    onMounted(() => {
      const isAuthenticated = localStorage.getItem('access_token');
      if (!isAuthenticated && router.currentRoute.value.path !== '/auth') {
        router.push('/auth');
      }
    });

    return {};
  },
};
</script>
