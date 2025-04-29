<template>
  <div class="profile-page">
    <!-- Колонка 1: Информация -->
    <div class="column user-info">
      <h2 style="text-align: center;">Информация о пользователе</h2>
      <p style="text-align: center;"><strong>Имя:</strong> {{ user.username }}</p>
      <p style="text-align: center;"><strong>Email:</strong> {{ user.email }}</p>

      <div class="button_logout">
        <button @click="logout">Выйти из аккаунта</button>
      </div>
    </div>

    <!-- Колонка 2: Логи -->
    <div class="column login-logs">
      <h2 style="text-align: center;">История входа в систему</h2>
      <div class="logs-scroll-container">
        <table>
          <thead>
            <tr>
              <th>Время</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(log, index) in logs" :key="index">
              <td>{{ formatDate(log.auth_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Колонка 3: Управление -->
    <div class="column account-actions">
      <h2 style="text-align: center;">Управление аккаунтом</h2>

      <!-- Смена пароля -->
      <label for="old-password">Старый пароль:</label>
      <input type="password" v-model="oldPassword" id="old-password" />

      <label for="new-password">Новый пароль:</label>
      <input type="password" v-model="newPassword" id="new-password" />



      <!-- Кнопки -->
      <div class="buttons">
      <button @click="changePassword">Сменить пароль</button>
        <button class="danger" @click="confirmDelete">Удалить аккаунт</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref({ username: '', email: '' })
const logs = ref([])
const oldPassword = ref('')
const newPassword = ref('')

onMounted(async () => {
  const token = localStorage.getItem('access_token')

  try {
    const userRes = await axios.get('http://localhost:8000/user/me', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = userRes.data

    const logsRes = await axios.get('http://localhost:8000/user/auth_logs', {
      headers: { Authorization: `Bearer ${token}` }
    })
    logs.value = logsRes.data
  } catch (err) {
    console.error('Ошибка загрузки:', err)
  }
})

const formatDate = (ts) => new Date(ts).toLocaleString()

const changePassword = async () => {
  const token = localStorage.getItem('access_token')
  try {
    await axios.put(
      'http://localhost:8000/user/change_password',
      {
        old: oldPassword.value,
        new: newPassword.value
      },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    alert('Пароль успешно изменён')
    oldPassword.value = ''
    newPassword.value = ''
  } catch (err) {
    alert('Ошибка при смене пароля')
    console.error(err)
  }
}

const logout = () => {
  localStorage.removeItem('access_token')
  router.push('/auth')
}

const confirmDelete = async () => {
  if (confirm('Вы уверены, что хотите удалить аккаунт? Это действие необратимо.')) {
    const token = localStorage.getItem('access_token')
    try {
      await axios.delete('http://localhost:8000/user/delete_account', {
        headers: { Authorization: `Bearer ${token}` }
      })
      localStorage.removeItem('access_token')
      router.push('/auth')
    } catch (err) {
      alert('Ошибка при удалении аккаунта')
      console.error(err)
    }
  }
}
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: row;
  gap: 10px;
  padding: 40px;
  background-color: #1e1e1e;
  color: #f1f1f1;
  min-height: 10vh;
  box-sizing: border-box;
  justify-content: space-between;
  flex-wrap: nowrap;
}

.column {
  flex: 1;
  min-width: 380px;
  background-color: #2c2c2c;
  padding: 20px;
  box-sizing: border-box;
}

.column h2 {
  margin-bottom: 20px;
  font-size: 16px;
  color: #f1f1f1;
}

.user-info p,
.account-actions label {
  margin-bottom: 5px;
  font-size: 14px;
}

input[type="password"] {
  width: 100%;
  padding: 8px;
  margin: 10px 0 15px;
  border-radius: 4px;
  border: 1px solid #444;
  background-color: #3a3a3a;
  color: #f1f1f1;
}

.login-logs table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.login-logs th,
.login-logs td {
  padding: 8px;
  border-bottom: 1px solid #444;
  text-align: left;
}

.logs-scroll-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #444;
  border-radius: 5px;
}

button {
  padding: 10px 15px;
  border: none;
  background-color: #444;
  color: #fff;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
}

button:hover {
  background-color: #666;
}

.buttons {
  display: flex;
  flex-direction: column;
  margin-top: 30px;
  gap: 10px;
}

.button_logout {
  display: flex;
  flex-direction: column;
  margin-top: 30px;
  gap: 10px;
}

.danger {
  background-color: #8b0000;
}

.danger:hover {
  background-color: #a00000;
}
</style>
