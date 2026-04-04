<template>
  <div class="update-container">
    <h2>Update Article</h2>

    <form v-if="article" @submit.prevent="updateArticle" class="update-form">
      <label for="title">Title</label>
      <input id="title" v-model="article.title" placeholder="Enter title" required />

      <label for="body">Body</label>
      <textarea id="body" v-model="article.body" placeholder="Enter body" required></textarea>

      <div class="buttons">
        <button type="submit" class="btn update-btn">Update</button>
        <button type="button" class="btn cancel-btn" @click="cancel">Cancel</button>
      </div>
    </form>

    <p v-else>Loading article...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const article = ref(null)

const API_URL = import.meta.env.VITE_API_URL 

const fetchArticle = async () => {
  try {
    const res = await axios.get(`${API_URL}/get/${route.params.id}/`)
    article.value = res.data
  } catch (err) {
    console.error(err)
  }
}

const updateArticle = async () => {
  try {
    await axios.put(`${API_URL}/update/${route.params.id}/`, article.value)
    router.push('/')
  } catch (err) {
    console.error(err)
  }
}

const cancel = () => router.push('/')

onMounted(fetchArticle)
</script>

<style scoped>
.update-container {
  max-width: 600px;
  margin: 30px auto;
  padding: 20px;
  border-radius: 8px;
  background-color: #f8f9fa;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  font-family: Arial, sans-serif;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 20px;
}

.update-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input, textarea {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 1rem;
  width: 100%;
  box-sizing: border-box;
}

textarea {
  resize: vertical;
  min-height: 120px;
}

.buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 10px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.update-btn {
  background-color: #3498db;
  color: white;
}

.update-btn:hover {
  background-color: #2980b9;
}

.cancel-btn {
  background-color: #e74c3c;
  color: white;
}

.cancel-btn:hover {
  background-color: #c0392b;
}
</style>