<template>
  <div v-if="article">
    <h1>{{ article.title }}</h1>
    <p>{{ article.body }}</p>
    <p><em>{{ article.date }}</em></p>
    <router-link :to="`/update/${article.id}`">Edit</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const article = ref(null)

onMounted(async () => {
  const res = await axios.get(`http://127.0.0.1:5001/get/${route.params.id}/`)
  article.value = res.data
})
</script>