<template>
  <div>
    <header><h1>Innihald</h1></header>

    <main>
      <div class="camera-placeholder"><Scan /></div>
      <div class="info">
        <p>Beindu símanum að strikamerki eða innihaldslýsingu.</p>
      </div>
    </main>

    <footer><button class="btn">Leita vörulista</button></footer>

    <nav class="fimmkassar">
      <RouterLink to="/">Forsíða</RouterLink>
      <RouterLink to="/about">Um vefinn</RouterLink>
    </nav>
  </div>
</template>

<script setup>
import Scan from "./scan.vue"; // file is "scan.vue" (lowercase)
</script>

<style scoped>
.camera-placeholder {
  border: 2px dashed #bbb;
  border-radius: 12px;
  padding: 0.5rem;
  min-height: 60vh;
  background: #000;
  display: grid;
  place-items: center;
}
.fimmkassar {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  padding: 1rem;
}
.fimmkassar a {
  display: block;
  text-align: center;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  text-decoration: none;
  color: #111;
  background: #fafafa;
}
.btn {
  padding: 0.6rem 1rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: #fff;
  cursor: pointer;
}
</style>
