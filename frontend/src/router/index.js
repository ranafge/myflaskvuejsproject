import { createRouter, createWebHistory } from 'vue-router';

import Home from '../components/Home.vue';
import ArticleList from '../components/ArticleList.vue';
import ArticleDetails from '../components/ArticleDetails.vue';
import AddArticle from '../components/AddArticle.vue';
import UpdateArticle from '../components/UpdateArticle.vue';
import DeleteArticle from '../components/DeleteArticle.vue';


const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/get', name: 'ArticleList', component: ArticleList },
  { path: '/article/:id', name: 'ArticleDetails', component: ArticleDetails },
  { path: '/add', name: 'AddArticle', component: AddArticle },
  { path: '/update/:id', name: 'UpdateArticle', component: UpdateArticle },
  { path: '/delete/:id', name: 'DeleteArticle', component: DeleteArticle },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;