<template>
  <div class="scanner">
    <!-- Camera preview -->
    <video ref="video" autoplay playsinline muted class="preview"></video>
    <!-- Hidden canvas for grabbing frames -->
    <canvas ref="canvas" class="hidden"></canvas>

    <div class="panel">
      <p class="status">{{ statusMsg }}</p>
      <button class="btn" @click="toggleScanning">
        {{ scanning ? "Stop scanning" : "Start scanning" }}
      </button>

      <div class="result" v-if="text">
        <h3>OCR Result</h3>
        <pre>{{ text }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import Tesseract from "tesseract.js";

const video = ref<HTMLVideoElement | null>(null);
const canvas = ref<HTMLCanvasElement | null>(null);
const text = ref<string>("");
const statusMsg = ref("Waiting for camera permission…");
const scanning = ref(false);

let stream: MediaStream | null = null;
let loopHandle: number | null = null;

// Start webcam
async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" }, // rear camera if available
      audio: false,
    });
    if (video.value) {
      video.value.srcObject = stream;
      await video.value.play();
      statusMsg.value = "Camera active.";
    }
  } catch (err) {
    statusMsg.value = "Failed to access camera. Check permissions.";
    console.error(err);
  }
}

// Run OCR on one frame
async function ocrOnce(): Promise<void> {
  if (!video.value || !canvas.value) return;
  const v = video.value;
  const c = canvas.value;

  const w = (c.width = Math.min(1024, v.videoWidth || 640));
  const h = (c.height = Math.floor(
    (w * (v.videoHeight || 480)) / (v.videoWidth || 640)
  ));

  const ctx = c.getContext("2d");
  if (!ctx) return;
  ctx.drawImage(v, 0, 0, w, h);

  statusMsg.value = "Recognizing text…";
  const { data } = await Tesseract.recognize(c, "eng+isl", {
    logger: (m) => {
      if (m.status) {
        statusMsg.value =
          m.status +
          (m.progress ? " " + Math.round(m.progress * 100) + "%" : "");
      }
    },
  });
  text.value = data.text?.trim() || "";
  statusMsg.value = "Frame processed.";
}

// Loop OCR every 2s
function loop() {
  loopHandle = window.setTimeout(async () => {
    await ocrOnce();
    if (scanning.value) loop();
  }, 2000);
}

// Toggle start/stop
function toggleScanning() {
  scanning.value = !scanning.value;
  if (scanning.value) {
    statusMsg.value = "Scanning started.";
    loop();
  } else {
    statusMsg.value = "Scanning stopped.";
    if (loopHandle) {
      clearTimeout(loopHandle);
      loopHandle = null;
    }
  }
}

// Lifecycle
onMounted(() => {
  startCamera();
  const ready = setInterval(() => {
    if (video.value?.readyState === 4) {
      clearInterval(ready);
      scanning.value = true;
      loop();
    }
  }, 250);
});

onBeforeUnmount(() => {
  if (loopHandle) clearTimeout(loopHandle);
  if (stream) stream.getTracks().forEach((t) => t.stop());
});
</script>

<style scoped>
.scanner {
  display: grid;
  gap: 1rem;
  justify-items: center;
}
.preview {
  width: min(640px, 95vw);
  border-radius: 12px;
  border: 2px solid #333;
}
.hidden {
  display: none;
}
.panel {
  width: min(640px, 95vw);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid #333;
  border-radius: 12px;
  padding: 0.75rem;
}
.status {
  opacity: 0.8;
  margin: 0 0 0.5rem;
}
.result {
  white-space: pre-wrap;
}
.btn {
  padding: 0.5rem 0.9rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
}
</style>
