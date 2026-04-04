<template>
  <div class="home-container">
    <div class="header">
      <h2>📝 All Articles</h2>
      <div class="article-count">{{ articles.length }} articles found</div>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>⏳ Loading articles...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error">
      <div class="error-icon">❌</div>
      <p>{{ error }}</p>
      <button @click="fetchArticles" class="retry-btn">🔄 Retry</button>
    </div>
    
    <!-- Articles List -->
    <div v-else class="articles-grid">
      <div class="article-card" v-for="article in articles" :key="article.id">
        <div class="article-header">
          <h3>{{ article.title }}</h3>
          <span class="article-id">#{{ article.id }}</span>
        </div>
        
        <div class="article-body">
          <p>{{ truncateText(article.body, 120) }}</p>
        </div>
        
        <div class="article-footer">
          <div class="article-date">
            📅 {{ formatDate(article.date) }}
          </div>
          <div class="card-buttons">
            <router-link :to="`/article/${article.id}`" class="btn view-btn" title="View Details">
              👁️ View
            </router-link>
            <router-link :to="`/update/${article.id}`" class="btn update-btn" title="Update Article">
              ✏️ Edit
            </router-link>
            <button @click="deleteArticle(article.id)" class="btn delete-btn" title="Delete Article">
              🗑️ Del
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="add-new-section">
      <router-link to="/add" class="add-btn">
        <span class="plus-icon">+</span> Add New Article
      </router-link>
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

const API_URL = import.meta.env.VITE_API_URL || 'http://192.168.0.100:5000'

console.log('📍 API URL:', API_URL)

const fetchArticles = async () => {
  loading.value = true
  error.value = null
  
  try {
    console.log('📡 Fetching articles from:', `${API_URL}/get`)
    const res = await axios.get(`${API_URL}/get`)
    articles.value = res.data
    console.log('✅ Loaded', articles.value.length, 'articles')
  } catch (err) {
    console.error('❌ Error fetching articles:', err)
    error.value = err.message || 'Failed to load articles'
  } finally {
    loading.value = false
  }
}

const deleteArticle = async (id) => {
  if (!confirm(`Are you sure you want to delete article #${id}?`)) return
  
  try {
    console.log('🗑️ Deleting article:', id)
    await axios.delete(`${API_URL}/delete/${id}/`)
    await fetchArticles()
  } catch (err) {
    console.error('❌ Delete failed:', err)
    alert('Failed to delete article')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'No date'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

onMounted(() => {
  console.log('🚀 Home component mounted')
  fetchArticles()
})
</script>

<style scoped>
/* Container Styles - No Background Color */
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  /* Removed background gradient */
}

/* Header Styles */
.header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header h2 {
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 28px;
}

.article-count {
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

/* Articles Grid */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

/* Article Card */
.article-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.article-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  flex: 1;
}

.article-id {
  background: rgba(255,255,255,0.2);
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.article-body {
  padding: 20px;
  flex: 1;
}

.article-body p {
  margin: 0;
  color: #555;
  line-height: 1.5;
  font-size: 14px;
}

.article-footer {
  padding: 15px 20px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.article-date {
  color: #888;
  font-size: 12px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 5px;
}

/* Card Buttons */
.card-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn {
  padding: 6px 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  color: white;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  transition: all 0.2s ease;
}

.view-btn {
  background-color: #2ecc71;
}

.view-btn:hover {
  background-color: #27ae60;
  transform: scale(1.05);
}

.update-btn {
  background-color: #3498db;
}

.update-btn:hover {
  background-color: #2980b9;
  transform: scale(1.05);
}

.delete-btn {
  background-color: #e74c3c;
}

.delete-btn:hover {
  background-color: #c0392b;
  transform: scale(1.05);
}

/* Add New Section */
.add-new-section {
  text-align: center;
  margin-top: 30px;
}

.add-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 30px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.25);
}

.plus-icon {
  font-size: 20px;
  font-weight: bold;
}

/* Loading State */
.loading {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error State */
.error {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
  color: #e74c3c;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.retry-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.retry-btn:hover {
  background: #2980b9;
}

/* Responsive Design */
@media (max-width: 768px) {
  .home-container {
    padding: 10px;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .card-buttons {
    justify-content: center;
  }
  
  .header h2 {
    font-size: 24px;
  }
}
</style>