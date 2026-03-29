<template>
  <div class="home-container">
    <h2>All Articles</h2>
    <div class="articles">
      <div class="article-card" v-for="article in articles" :key="article.id">
        <h3>{{ article.title }}</h3>
        <p>{{ article.body }}</p>
        <small>{{ formatDate(article.date) }}</small>
        <div class="card-buttons">
          <button @click="goToUpdate(article.id)" class="btn update-btn">Update</button>
          <button @click="deleteArticle(article.id)" class="btn delete-btn">Delete</button>
        </div>
      </div>
    </div>
    <div class="add-new">
      <router-link to="/add" class="btn add-btn">Add New Article</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const articles = ref([])
const router = useRouter()

const fetchArticles = async () => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/get`)
    articles.value = res.data
  } catch (err) {
    console.error(err)
  }
}

const goToUpdate = (id) => router.push(`/update/${id}`)

const deleteArticle = async (id) => {
  if (!confirm('Are you sure you want to delete this article?')) return
  try {
    await axios.delete(`${import.meta.env.VITE_API_URL}/delete/${id}/`)
    fetchArticles() // Refresh list
  } catch (err) {
    console.error(err)
  }
}

const formatDate = (dateStr) => new Date(dateStr).toLocaleString()

onMounted(fetchArticles)
</script>

<style scoped>
.home-container {
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
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.article-card {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.article-card h3 {
  margin: 0 0 10px 0;
  color: #34495e;
}

.article-card p {
  flex-grow: 1;
  color: #555;
  margin-bottom: 10px;
}

.article-card small {
  color: #888;
  margin-bottom: 10px;
  display: block;
}

.card-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.btn {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  color: white;
}

.update-btn {
  background-color: #3498db;
}

.update-btn:hover {
  background-color: #2980b9;
}

.delete-btn {
  background-color: #e74c3c;
}

.delete-btn:hover {
  background-color: #c0392b;
}

.add-new {
  text-align: center;
  margin-top: 30px;
}

.add-btn {
  background-color: #2ecc71;
  color: white;
  padding: 10px 25px;
  border-radius: 5px;
  text-decoration: none;
}

.add-btn:hover {
  background-color: #27ae60;
}
</style>