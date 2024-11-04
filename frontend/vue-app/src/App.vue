<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">VR Software</a>
        <router-link to="/produto" class="nav-link">Produtos</router-link>
      </div>
    </nav>
    <main class="container mt-4">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  background-color: #f8f9fa;
}
</style>
