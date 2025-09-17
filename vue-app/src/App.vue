<template>
  <section class="page">
    <header>
      <h1>Innihald</h1>
    </header>

    <main>
      <div class="camera-placeholder">
        <!-- CAMERA + OCR -->
        <TextScanner />
      </div>

      <div class="info">
        <p>Beindu símanum að strikamerki eða innihaldslýsingu.</p>
      </div>
    </main>

    <footer>
      <button class="btn">Leit</button>
    </footer>

    <nav class="fimmkassar">
      <a :href="paths.kort" :class="{ active: isActive('kort.html') }">
        <img src="/myndir/kort mynd.png" alt="Kort" />
      </a>

      <a
        :href="paths.samanburdur"
        :class="{ active: isActive('samanburður.html') }"
      >
        <img src="/myndir/berasamann.png" alt="berasamann" />
      </a>

      <a :href="paths.forsida" :class="{ active: isActive('forsíða.html') }">
        <img src="/myndir/borða.png" alt="scan" />
      </a>

      <a :href="paths.user" :class="{ active: isActive('user.html') }">
        <img src="/myndir/user.png" alt="user" />
      </a>

      <a :href="paths.baeta" :class="{ active: isActive('bætaviðvoru.html') }">
        <!-- má bæta inn mynd síðar -->
      </a>
    </nav>
  </section>
</template>

<script setup lang="ts">
import TextScanner from "@/components/scanner/TextScanner.vue";

const paths = {
  kort: "kort.html",
  samanburdur: "samanburður.html",
  forsida: "forsíða.html",
  user: "user.html",
  baeta: "bætaviðvoru.html",
};

function isActive(file: string) {
  const current = decodeURI(location.pathname.split("/").pop() || "index.html");
  return decodeURI(file) === current;
}
</script>

<style scoped>
.page {
  min-height: 100dvh;
  display: grid;
  grid-template-rows: auto 1fr auto auto;
}

.camera-placeholder {
  display: grid;
  place-items: center;
  min-height: 40vh;
  border: 2px dashed #ccc;
  border-radius: 12px;
  margin: 1rem;
  padding: 0.75rem;
}

.fimmkassar {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
  padding: 0.75rem 1rem 1.25rem;
}

.fimmkassar a {
  display: grid;
  place-items: center;
  padding: 0.5rem;
  border-radius: 12px;
  text-decoration: none;
  border: 1px solid transparent;
}

.fimmkassar a.active {
  border-color: #888;
  outline: 2px solid #888;
}

.fimmkassar img {
  max-width: 100%;
  height: 56px;
  object-fit: contain;
}

.btn {
  padding: 0.65rem 1rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
}
</style>
