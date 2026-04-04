<template>
  <div class="add-container">
    <h2>Add New Article</h2>

    <form @submit.prevent="addArticle" class="add-form">
      <label for="title">Title</label>
      <input
        id="title"
        v-model="title"
        placeholder="Enter article title"
        required
      />

      <label for="body">Body</label>
      <textarea
        id="body"
        v-model="body"
        placeholder="Enter article body"
        required
      ></textarea>

      <div class="buttons">
        <button type="submit" class="btn add-btn">Add Article</button>
        <button type="button" class="btn cancel-btn" @click="cancel">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const title = ref('')
const body = ref('')
const router = useRouter()

const API_URL = import.meta.env.VITE_API_URL 
const addArticle = async () => {
  try {
    await axios.post(`${API_URL}/add`, {
      title: title.value,
      body: body.value
    })
    router.push('/')
  } catch (err) {
    console.error(err)
  }
}

const cancel = () => router.push('/')
</script>

<style scoped>
.add-container {
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

.add-form {
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

.add-btn {
  background-color: #2ecc71;
  color: white;
}

.add-btn:hover {
  background-color: #27ae60;
}

.cancel-btn {
  background-color: #e74c3c;
  color: white;
}

.cancel-btn:hover {
  background-color: #c0392b;
}
</style>
