<template>
  <div class="auth-wrapper">
    <!-- Прозрачный спейсер с динамической шириной -->
    <div :style="{ width: spacerWidth + 'px' }" class="spacer"></div>

    <!-- Контейнер с формой -->
    <div class="auth-container">
      <!-- Вкладки -->
      <div class="tabs">
        <button
          :class="{'active': activeTab === 'login'}"
          @click="activeTab = 'login'">Авторизация</button>
        <button
          :class="{'active': activeTab === 'register'}"
          @click="activeTab = 'register'">Регистрация</button>
      </div>

      <!-- Вкладка "Авторизация" -->
      <div v-if="activeTab === 'login'" class="tab-content">
        <h2 class="auth-title">Авторизация</h2>
        <input
          type="text"
          v-model="username"
          class="auth-input"
          placeholder="Логин"
        />
        <input
          type="password"
          v-model="password"
          class="auth-input"
          placeholder="Пароль"
        />
        <button @click="authenticate" class="auth-button">Войти</button>
        <p v-if="authError" class="auth-error">{{ authError }}</p>
      </div>

      <!-- Вкладка "Регистрация" -->
      <div v-if="activeTab === 'register'" class="tab-content">
        <h2 class="auth-title">Регистрация</h2>
        <input
          type="text"
          v-model="registerLogin"
          class="auth-input"
          placeholder="Логин"
        />
        <input
          type="password"
          v-model="registerPassword"
          class="auth-input"
          placeholder="Пароль"
        />
        <input
          type="text"
          v-model="registerEmail"
          class="auth-input"
          placeholder="Email"
        />
        <button @click="register" class="auth-button">Зарегистрироваться</button>
        <p v-if="registerError" class="auth-error">{{ registerError }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'Auth',
  data() {
    return {
      activeTab: 'login', // Вкладка по умолчанию - авторизация
      username: '',
      password: '',
      registerLogin: '',
      registerPassword: '',
      registerEmail: '',
      authError: '',
      registerError: '',
      spacerWidth: 400, // Изначальная ширина спейсера
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    async authenticate() {
    try {
      // Формируем данные для отправки в формате x-www-form-urlencoded
      const formData = new URLSearchParams();
      formData.append('username', this.username);
      formData.append('password', this.password);
      formData.append('grant_type', 'password'); // Указываем тип авторизации

      // Выполняем POST запрос с данными для авторизации через OAuth2
      const response = await axios.post('http://localhost:8000/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      const accessToken = response.data.access_token;
      localStorage.setItem('access_token', accessToken); // Сохраняем токен

      // После успешной авторизации отправляем запрос для записи логов
      await axios.post('http://localhost:8000/user/auth_logs', {
        auth_at: Date.now()
      }, {
        headers: {
          Authorization: `Bearer ${accessToken}` // Передаем токен авторизации
        }
      });

      // Перенаправляем на главную страницу
      this.router.push('/');

    } catch (error) {
      console.error('Auth error:', error);
      this.authError = 'Неверный логин или пароль';
    }
  },
    async register() {
      try {
        const response = await axios.post('http://localhost:8000/auth/register', {
          username: this.registerLogin,
          password: this.registerPassword,
          email: this.registerEmail
        });

        console.log('Registration successful:', response.data);
        this.registerError = 'Вы успешно зарегистрировались в системе!';
        this.registerLogin = '';
        this.registerPassword = '';
        this.registerEmail = '';
      } catch (error) {
        console.error('Registration error:', error);
        this.registerError = 'Ошибка при регистрации';
      }
    }
  }
};
</script>

<style scoped>
/* Родительский контейнер */
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

body {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #121212;
}

/* Контейнер с оберткой (для выравнивания и спейсера) */
.auth-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

/* Прозрачный спейсер */
.spacer {
  background-color: transparent;
  height: 100%;
  transition: width 0.3s ease;
}

/* Контейнер с формой */
.auth-container {
  background-color: #121212;
  color: #f1f1f1;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
}

/* Вкладки */
.tabs {
  display: flex;
  width: 100%;
  margin-bottom: 20px;
  border-bottom: 2px solid #444;
}

.tabs button {
  padding: 10px;
  background-color: #333;
  color: #f1f1f1;
  border: 1px solid #444;
  border-radius: 5px 5px 0 0;
  cursor: pointer;
  transition: background-color 0.3s ease;
  text-align: center;
  flex-grow: 1;
}

.tabs button.active {
  background-color: #555;
  border-bottom: 2px solid #f1f1f1;
}

/* Стиль контента вкладок */
.tab-content {
  display: block;
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.auth-title {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
  color: #f1f1f1;
}

.auth-input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  background-color: #333;
  color: #f1f1f1;
  border: 1px solid #444;
  border-radius: 5px;
}

.auth-input:focus {
  border-color: #888;
  outline: none;
}

.auth-button {
  width: 100%;
  padding: 10px;
  background-color: #444;
  color: #f1f1f1;
  border: 1px solid #555;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.auth-button:hover {
  background-color: #666;
}

.auth-error {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>
