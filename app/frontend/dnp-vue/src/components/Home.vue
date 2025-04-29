<template>
  <div class="container">
    <!-- Левая панель -->
    <div class="sidebar">
      <h3></h3>
      <div class="table-container">
        <table v-if="results.length">
          <thead>
            <tr>
              <th>Результат</th>
              <th>Время</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entry, index) in results" :key="index">
              <td>{{ entry.data }}</td>
              <td>{{ formatTimestamp(entry.timestamp) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else style="text-align: center;">Список результатов пуст</p>
      </div>
      <button @click="deleteResults">Очистить результаты</button>
    </div>

    <!-- Основной контент -->
    <div class="main">
      <h2 style="text-align: right; font-size: 14px;">NET-лист</h2>
      <textarea v-model="text" rows="10" cols="80"></textarea>

      <div class="input-container">
        <!-- Однострочное поле ввода -->
        <input type="text" v-model="inputField" placeholder="Объект поиска" />
      </div>



      <h2 style="text-align: right; font-size: 14px;">Результат</h2>
      <textarea v-model="result" rows="10" cols="80" readonly></textarea>
      <button @click="sendText">Начать парсинг</button>
      <div style="height: 3px;"></div>
      <button @click="goToProfile">Перейти в профиль</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      text: "",
      result: "",
      results: [],
      inputField: "" // Добавляем переменную для однострочного поля
    };
  },
  mounted() {
    this.loadResults();
  },
  methods: {
    async sendText() {
      const token = localStorage.getItem('access_token');

      const response = await fetch("http://localhost:8000/parse/netlist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ text: this.text, obj_name: this.inputField }),
      });

      if (response.ok) {
        const parsed = await response.json();
        this.result = parsed.result;
        console.log(parsed);

        // Отправим результат в историю
        await fetch("http://localhost:8000/user/results", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
          },
          body: JSON.stringify({
            data: this.result,
            timestamp: Date.now(),
          }),
        });

        this.loadResults();
      } else {
        this.result = "Ошибка при обработке запроса";
        console.error("Ошибка:", response.statusText);
      }
    },

    async loadResults() {
      try {
        const token = localStorage.getItem('access_token');
        const res = await fetch("http://localhost:8000/user/results", {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });
        if (!res.ok) throw new Error("Ошибка при получении истории");
        this.results = await res.json();
      } catch (e) {
        console.error(e);
      }
    },

    async deleteResults() {
      const token = localStorage.getItem('access_token');
      try {
        const response = await fetch("http://localhost:8000/user/delete_results", {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });
        this.loadResults();
      } catch (err) {
        alert('Ошибка при удалении результатов');
        console.error(err);
      }
    },

    goToProfile() {
      this.$router.push("/profile");
    },

    formatTimestamp(ts) {
      return new Date(ts).toLocaleString();
    }
  }
};
</script>

<style scoped>
/* Темная тема */
.container {
  display: flex;
  flex-direction: row;
  background-color: #121212; /* Темный фон для всего контейнера */
  color: #f1f1f1; /* Светлый текст */
  min-width: 100%; /* Убедитесь, что контейнер занимает все доступное пространство */
}

.sidebar {
  width: 600px;
  flex-shrink: 0; /* Запрещаем сжатие */
  min-width: 600px; /* Устанавливаем минимальную ширину */
  border-right: 1px solid #444; /* Тёмная граница */
  padding: 0px;
  background-color: #333; /* Темный фон для левой панели */
  overflow-y: auto;
}

.table-container {
  max-height: 600px;
  overflow-y: auto;
  margin-bottom: 1px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  background-color: #2a2a2a; /* Тёмный фон для таблицы */
}

th, td {
  border: 1px solid #444; /* Тёмные границы ячеек */
  padding: 8px;
  text-align: left;
  color: #f1f1f1; /* Светлый текст в ячейках */
}

th {
  background-color: #333; /* Темный фон для заголовков таблицы */
  position: sticky;
  top: 0;
}

.main {
  flex-grow: 1;
  padding: 20px;
  background-color: #181818; /* Темный фон для основного контента */
  color: #f1f1f1; /* Светлый текст в основном контенте */
  min-width: 600px; /* Установите минимальную ширину, чтобы контент не сжимался */
}

button {
  width: 100%;
  padding: 10px;
  background-color: #444;
  color: #f1f1f1;
  border: 1px solid #555;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #666; /* Светлее фон на кнопках при наведении */
}

textarea {
  background-color: #333; /* Тёмный фон для текстовых областей */
  color: #f1f1f1; /* Светлый текст */
  border: 1px solid #444; /* Тёмные границы */
  padding: 10px;
  width: 100%;
  resize: none;
}

textarea:focus {
  border-color: #888; /* Ярче граница при фокусе */
  outline: none;
}

p {
  color: #ccc; /* Светлый текст для сообщений */
}

.input-container {
  margin-top: 10px;
  margin-bottom: 20px;
}

input[type="text"] {
  width: 100%;
  padding: 8px;
  background-color: #333;
  color: #f1f1f1;
  border: 1px solid #444;
  border-radius: 5px;
}

input[type="text"]:focus {
  border-color: #888;
  outline: none;
}
</style>
