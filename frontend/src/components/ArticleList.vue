<!-- src/components/ArticleList.vue -->
<template>
  <div class="article-list-container">
    <h2>All Articles</h2>
    
    <div v-if="loading" class="loading">
      ⏳ Loading articles...
    </div>
    
    <div v-else-if="error" class="error">
      ❌ {{ error }}
    </div>
    
    <div v-else class="articles">
      <div class="article-card" v-for="article in articles" :key="article.id">
        <h3>{{ article.title }}</h3>
        <p>{{ article.body.substring(0, 100) }}...</p>
        <small>{{ formatDate(article.date) }}</small>
        <div class="card-buttons">
          <router-link :to="`/article/${article.id}`" class="btn view-btn">
            👁️ View Details
          </router-link>
          <router-link :to="`/update/${article.id}`" class="btn update-btn">
            ✏️ Update
          </router-link>
          <button @click="deleteArticle(article.id)" class="btn delete-btn">
            🗑️ Delete
          </button>
        </div>
      </div>
    </div>
    
    <div class="add-new">
      <router-link to="/add" class="btn add-btn">+ Add New Article</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const articles = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()

const API_URL = import.meta.env.VITE_API_URL

const fetchArticles = async () => {
  loading.value = true
  error.value = null
  
  try {
    const res = await axios.get(`${API_URL}/get`)
    articles.value = res.data
    console.log('✅ Loaded', articles.value.length, 'articles')
  } catch (err) {
    console.error('❌ Error:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const deleteArticle = async (id) => {
  if (!confirm('Are you sure?')) return
  try {
    await axios.delete(`${API_URL}/delete/${id}/`)
    await fetchArticles()
  } catch (err) {
    console.error(err)
    alert('Delete failed')
  }
}

const formatDate = (dateStr) => new Date(dateStr).toLocaleString()

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.article-list-container {
  max-width: 900px;
  margin: 30px auto;
  font-family: Arial, sans-serif;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #2c3e50;
}

.articles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.article-card {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.article-card h3 {
  margin: 0 0 10px 0;
  color: #34495e;
}

.article-card p {
  color: #555;
  margin-bottom: 10px;
}

.article-card small {
  color: #888;
  display: block;
  margin-bottom: 10px;
}

.card-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  color: white;
  text-decoration: none;
  font-size: 12px;
}

.view-btn {
  background-color: #2ecc71;
}
.update-btn {
  background-color: #3498db;
}
.delete-btn {
  background-color: #e74c3c;
}
.add-btn {
  background-color: #2ecc71;
  color: white;
  padding: 10px 25px;
  border-radius: 5px;
  text-decoration: none;
}

.add-new {
  text-align: center;
  margin-top: 30px;
}

.loading, .error {
  text-align: center;
  padding: 50px;
}
.error {
  color: #e74c3c;
}
</style>