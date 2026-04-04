<template>
  <div class="article-detail-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>⏳ Loading article...</p>
    </div>
    
    <!-- 404 Not Found State -->
    <div v-else-if="notFound" class="not-found">
      <div class="not-found-icon">🔍</div>
      <h1>404 - Article Not Found</h1>
      <p>Sorry, the article with ID "{{ articleId }}" does not exist in our database.</p>
      <div class="suggestions">
        <p>📝 Available article IDs: {{ availableIds.join(', ') }}</p>
        <p>💡 Try one of these IDs instead:</p>
        <div class="suggested-links">
          <router-link 
            v-for="id in availableIds.slice(0, 5)" 
            :key="id" 
            :to="`/article/${id}`"
            class="suggested-link"
          >
            Article #{{ id }}
          </router-link>
        </div>
      </div>
      <div class="actions">
        <router-link to="/" class="btn home-btn">
          🏠 Back to Home
        </router-link>
        <router-link to="/add" class="btn add-btn">
          ➕ Add New Article
        </router-link>
      </div>
    </div>
    
    <!-- Error State (Other Errors) -->
    <div v-else-if="error" class="error">
      <div class="error-icon">❌</div>
      <h2>Error Loading Article</h2>
      <p>{{ error }}</p>
      <button @click="fetchArticle" class="retry-btn">🔄 Try Again</button>
      <router-link to="/" class="btn home-btn">🏠 Go Home</router-link>
    </div>
    
    <!-- Article Found State -->
    <div v-else-if="article" class="article-detail">
      <div class="article-header">
        <h1>{{ article.title }}</h1>
        <span class="article-id">#{{ article.id }}</span>
      </div>
      
      <div class="article-meta">
        <div class="meta-item">
          <span class="meta-label">📅 Published:</span>
          <span class="meta-value">{{ formatDate(article.date) }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">🆔 Article ID:</span>
          <span class="meta-value">{{ article.id }}</span>
        </div>
      </div>
      
      <div class="article-content">
        <h3>📖 Content</h3>
        <p>{{ article.body }}</p>
      </div>
      
      <div class="article-actions">
        <router-link :to="`/update/${article.id}`" class="btn edit-btn">
          ✏️ Edit Article
        </router-link>
        <button @click="deleteArticle" class="btn delete-btn">
          🗑️ Delete Article
        </button>
        <router-link to="/" class="btn back-btn">
          ← Back to Home
        </router-link>
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
const notFound = ref(false)
const availableIds = ref([])

const API_URL = import.meta.env.VITE_API_URL || 'http://192.168.0.100:5000'
const articleId = route.params.id

console.log('🔍 ArticleDetails - Looking for ID:', articleId)

// Fetch all articles to get available IDs
const fetchAvailableIds = async () => {
  try {
    const res = await axios.get(`${API_URL}/get`)
    availableIds.value = res.data.map(a => a.id)
    console.log('📋 Available IDs:', availableIds.value)
  } catch (err) {
    console.error('Failed to fetch available IDs:', err)
  }
}

const fetchArticle = async () => {
  loading.value = true
  error.value = null
  notFound.value = false
  
  try {
    const url = `${API_URL}/get/${articleId}/`
    console.log('📡 Fetching:', url)
    
    const res = await axios.get(url)
    
    // Check if article exists
    if (res.data && Object.keys(res.data).length > 0 && !res.data.error) {
      article.value = res.data
      console.log('✅ Article found:', article.value.title)
    } else {
      // Article not found
      notFound.value = true
      console.log('❌ Article not found for ID:', articleId)
      await fetchAvailableIds()
    }
  } catch (err) {
    console.error('❌ Error:', err)
    
    // Check if it's a 404 error
    if (err.response && err.response.status === 404) {
      notFound.value = true
      await fetchAvailableIds()
    } else if (err.code === 'ERR_NETWORK') {
      error.value = 'Cannot connect to server. Please make sure Flask is running.'
    } else {
      error.value = err.message || 'Failed to load article'
    }
  } finally {
    loading.value = false
  }
}

const deleteArticle = async () => {
  if (!confirm(`Are you sure you want to delete "${article.value.title}"?`)) return
  
  try {
    await axios.delete(`${API_URL}/delete/${article.value.id}/`)
    router.push('/')
  } catch (err) {
    console.error('Delete failed:', err)
    alert('Failed to delete article')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'No date'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
.article-detail-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Loading State */
.loading {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
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

/* 404 Not Found State */
.not-found {
  text-align: center;
  padding: 60px 40px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.not-found-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.not-found h1 {
  color: #e74c3c;
  margin-bottom: 15px;
  font-size: 48px;
}

.not-found p {
  color: #666;
  font-size: 18px;
  margin-bottom: 30px;
}

.suggestions {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
  text-align: left;
}

.suggestions p {
  margin: 10px 0;
  font-size: 14px;
}

.suggested-links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
}

.suggested-link {
  display: inline-block;
  padding: 8px 16px;
  background: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.suggested-link:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

/* Error State */
.error {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.error-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.error h2 {
  color: #e74c3c;
  margin-bottom: 15px;
}

/* Article Found State */
.article-detail {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.article-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-header h1 {
  margin: 0;
  font-size: 28px;
  flex: 1;
}

.article-id {
  background: rgba(255,255,255,0.2);
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.article-meta {
  padding: 20px 30px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  gap: 10px;
}

.meta-label {
  font-weight: 600;
  color: #555;
}

.meta-value {
  color: #888;
}

.article-content {
  padding: 30px;
}

.article-content h3 {
  margin-top: 0;
  color: #2c3e50;
  margin-bottom: 15px;
}

.article-content p {
  line-height: 1.6;
  color: #555;
  font-size: 16px;
  white-space: pre-wrap;
}

.article-actions {
  padding: 20px 30px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

/* Button Styles */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.edit-btn {
  background-color: #3498db;
  color: white;
}

.edit-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

.delete-btn {
  background-color: #e74c3c;
  color: white;
}

.delete-btn:hover {
  background-color: #c0392b;
  transform: translateY(-2px);
}

.back-btn, .home-btn {
  background-color: #95a5a6;
  color: white;
}

.back-btn:hover, .home-btn:hover {
  background-color: #7f8c8d;
  transform: translateY(-2px);
}

.add-btn {
  background-color: #2ecc71;
  color: white;
}

.add-btn:hover {
  background-color: #27ae60;
  transform: translateY(-2px);
}

.retry-btn {
  margin: 10px;
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.retry-btn:hover {
  background: #2980b9;
}

.actions {
  margin-top: 20px;
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

/* Responsive Design */
@media (max-width: 768px) {
  .article-detail-container {
    padding: 10px;
  }
  
  .article-header {
    padding: 20px;
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  
  .article-header h1 {
    font-size: 22px;
  }
  
  .article-meta {
    flex-direction: column;
    gap: 10px;
  }
  
  .article-actions {
    flex-direction: column;
  }
  
  .btn {
    justify-content: center;
  }
  
  .not-found h1 {
    font-size: 32px;
  }
}
</style>