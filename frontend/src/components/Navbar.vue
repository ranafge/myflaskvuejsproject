<template>
  <nav>
    <ul>
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/add">Add New Article</router-link></li>
    </ul>
  </nav>
</template>

<style>
nav {
  background-color: #2c3e50;
  padding: 10px;
}
nav ul {
  display: flex;
  gap: 15px;
  list-style: none;
  color: white;
}
nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}
nav a.router-link-active {
  text-decoration: underline;
}
</style>