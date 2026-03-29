<template>
  <div class="delete-container">
    <div class="delete-card">
      <h2>🗑️ Delete Article</h2>
      <div v-if="loading">Loading...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else>
        <p class="warning">⚠️ Are you sure you want to delete "{{ article?.title }}"?</p>
        <div class="buttons">
          <button @click="deleteArticle" class="btn btn-danger">Yes, Delete</button>
          <button @click="cancel" class="btn btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const article = ref(null)
const loading = ref(true)
const error = ref(null)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

const fetchArticle = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${API_URL}/get/${route.params.id}/`)
    article.value = res.data
  } catch (err) {
    error.value = 'Failed to load article'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const deleteArticle = async () => {
  try {
    await axios.delete(`${API_URL}/delete/${route.params.id}/`)
    router.push('/')
  } catch (err) {
    error.value = 'Failed to delete article'
    console.error(err)
  }
}

const cancel = () => router.push('/')

onMounted(fetchArticle)
</script>

<style scoped>
.delete-container{max-width:500px;margin:50px auto;padding:20px}
.delete-card{background:white;border-radius:8px;padding:30px;box-shadow:0 2px 10px rgba(0,0,0,0.1);text-align:center}
h2{color:#e74c3c;margin-bottom:20px}
.error{color:#e74c3c;background:#fde0e0;padding:15px;border-radius:4px}
.warning{color:#e67e22;font-size:18px;margin-bottom:20px}
.buttons{display:flex;gap:15px;justify-content:center;margin-top:20px}
.btn{padding:10px 20px;border:none;border-radius:5px;cursor:pointer;font-size:16px}
.btn-danger{background:#e74c3c;color:white}
.btn-secondary{background:#95a5a6;color:white}
.btn-danger:hover{background:#c0392b}
.btn-secondary:hover{background:#7f8c8d}
</style>