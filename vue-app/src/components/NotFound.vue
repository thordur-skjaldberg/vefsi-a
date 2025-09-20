<template>
  <div class="not-found">
    <h1>404</h1>
    <p>Því miður fannst síðan ekki.</p>
    <router-link to="/">Fara á forsíðu</router-link>
  </div>
</template>

<script setup lang="ts">
// ekkert sérstakt þarf hér
</script>

<style scoped>
.not-found {
  text-align: center;
  margin-top: 50px;
}
h1 {
  font-size: 4rem;
  color: red;
}
</style>
