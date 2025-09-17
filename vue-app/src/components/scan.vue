<template>
  <div class="w-full max-w-screen-sm mx-auto p-4 space-y-3">
    <h2 class="text-xl font-bold">Lifunarskanni – Texti</h2>

    <!-- Myndavélin er opin allan tímann meðan "scanning" er sönn -->
    <div class="relative rounded-xl overflow-hidden bg-black aspect-[3/4]">
      <video
        ref="videoEl"
        autoplay
        playsinline
        muted
        class="w-full h-full object-cover"
      ></video>

      <!-- Létt "guideline" fyrir miðju (ROI) -->
      <div class="absolute inset-0 pointer-events-none grid place-items-center">
        <div
          class="rounded-xl border-2 border-white/60 backdrop-blur-[1px]"
          :style="roiStyle"
          title="Svæði sem er skannað í hverri lotu"
        ></div>
      </div>

      <!-- Staða -->
      <div
        class="absolute bottom-2 left-2 text-xs bg-black/60 text-white px-2 py-1 rounded"
      >
        {{ status }}
      </div>
    </div>

    <div class="flex items-center gap-2">
      <button class="btn" @click="toggleScan">
        {{ scanning ? "Pása skönnun" : "Ræsa skönnun" }}
      </button>

      <label class="btn">
        Hlaða upp mynd
        <input type="file" accept="image/*" class="hidden" @change="onFile" />
      </label>

      <label class="flex items-center gap-2 text-sm">
        <input type="checkbox" v-model="highAccuracy" />
        Nákvæmara (hægara)
      </label>
    </div>

    <details open class="rounded-xl border p-3 bg-white">
      <summary class="font-medium cursor-pointer">Niðurstöður (OCR)</summary>
      <pre class="whitespace-pre-wrap break-words mt-2">{{
        ocrText || "—"
      }}</pre>
    </details>

    <!-- falinn vinnsludúkur -->
    <canvas ref="canvasEl" class="hidden"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import Tesseract from "tesseract.js";

const videoEl = ref(null);
const canvasEl = ref(null);

const scanning = ref(true);
const status = ref("Ræði upp…");
const ocrText = ref("");
const workerRef = ref(null);
const loopHandle = ref(null);

const highAccuracy = ref(false);

// ROI (svæði sem við skerum út til hraðari OCR)
const roiPercent = { w: 0.9, h: 0.35 }; // 90% breidd, 35% hæð í miðju
const roiStyle = computed(() => {
  return {
    width: `${roiPercent.w * 100}%`,
    height: `${roiPercent.h * 100}%`,
  };
});

async function initCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: { ideal: "environment" }, // aftari myndavél
      },
      audio: false,
    });
    videoEl.value.srcObject = stream;
    await videoEl.value.play();
  } catch (err) {
    status.value = "🔥 Gat ekki opnað myndavél (þarftu HTTPS/heimild?)";
    console.error(err);
  }
}

async function initWorker() {
  status.value = "Hleð OCR (Tesseract)…";
  // Nota bæði ensku og íslensku – Tesseract sækir sjálfkrafa traineddata af CDN
  // Þú getur sett 'eng' ef þú vilt hraðara
  workerRef.value = await Tesseract.createWorker("eng+isl");
  status.value = "OCR tilbúið";
}

function getRoiFrame(ctx, vw, vh) {
  // reikna ROI miðjað
  const rw = Math.floor(vw * roiPercent.w);
  const rh = Math.floor(vh * roiPercent.h);
  const rx = Math.floor((vw - rw) / 2);
  const ry = Math.floor((vh - rh) / 2);
  const imageData = ctx.getImageData(rx, ry, rw, rh);
  // teikna ROI yfir á minnkaðan striga til hraðari OCR
  const maxW = highAccuracy.value ? 1280 : 768;
  const scale = Math.min(1, maxW / rw);
  const tw = Math.max(64, Math.floor(rw * scale));
  const th = Math.max(64, Math.floor(rh * scale));

  const tmp = document.createElement("canvas");
  tmp.width = tw;
  tmp.height = th;
  const tctx = tmp.getContext("2d");
  // setjum upp í tmp-canvas
  const off = document.createElement("canvas");
  off.width = rw;
  off.height = rh;
  off.getContext("2d").putImageData(imageData, 0, 0);
  tctx.drawImage(off, 0, 0, tw, th);
  return tmp;
}

async function recognizeCanvas(can) {
  if (!workerRef.value) return "";
  const { data } = await workerRef.value.recognize(can, {
    // stillingar sem jafna hraða/niðurstöðu
    tessedit_char_whitelist: undefined, // stilltu ef þú vilt aðeins tölustafi o.þ.h.
  });
  return data && data.text ? data.text.trim() : "";
}

async function scanTick() {
  if (!scanning.value) return;

  const vid = videoEl.value;
  const can = canvasEl.value;
  if (!vid || !vid.videoWidth) {
    // myndavél ekki tilbúin enn
    loopHandle.value = setTimeout(scanTick, 400);
    return;
  }

  // Teiknum ramma á striga
  const vw = vid.videoWidth;
  const vh = vid.videoHeight;
  can.width = vw;
  can.height = vh;
  const ctx = can.getContext("2d");
  ctx.drawImage(vid, 0, 0, vw, vh);

  // Skerum út ROI og minnkum
  const roiCanvas = getRoiFrame(ctx, vw, vh);

  try {
    status.value = "Les texta…";
    const text = await recognizeCanvas(roiCanvas);
    if (text) {
      ocrText.value = text;
      status.value = "Lesið ✔";
    } else {
      status.value = "Enginn texti fannst";
    }
  } catch (e) {
    console.error(e);
    status.value = "Villa í OCR";
  } finally {
    // Þéttum ekki of mikið: ~1.5–3 sek milli lota (háð nákvæmni)
    const delay = highAccuracy.value ? 2500 : 1200;
    loopHandle.value = setTimeout(scanTick, delay);
  }
}

function toggleScan() {
  scanning.value = !scanning.value;
  if (scanning.value) {
    status.value = "Skanna…";
    scanTick();
  } else {
    status.value = "Pásað";
    if (loopHandle.value) clearTimeout(loopHandle.value);
  }
}

async function onFile(e) {
  const file = e.target.files?.[0];
  if (!file) return;
  status.value = "Les upphlaðna mynd…";
  const img = new Image();
  img.onload = async () => {
    const can = document.createElement("canvas");
    can.width = img.width;
    can.height = img.height;
    const ctx = can.getContext("2d");
    ctx.drawImage(img, 0, 0);
    try {
      const text = await recognizeCanvas(can);
      ocrText.value = text || "";
      status.value = text ? "Lesið úr mynd ✔" : "Enginn texti fannst í mynd";
    } catch (err) {
      console.error(err);
      status.value = "Villa í OCR á mynd";
    }
  };
  img.src = URL.createObjectURL(file);
}

onMounted(async () => {
  await initCamera();
  await initWorker();
  if (scanning.value) scanTick();
});

onBeforeUnmount(() => {
  if (loopHandle.value) clearTimeout(loopHandle.value);
  if (videoEl.value?.srcObject) {
    for (const track of videoEl.value.srcObject.getTracks()) track.stop();
  }
});
</script>

<style scoped>
.btn {
  @apply px-3 py-2 rounded-lg border bg-white hover:bg-gray-50 active:scale-[.98];
}
</style>
