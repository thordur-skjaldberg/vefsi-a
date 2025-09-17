<!DOCTYPE html>
<link rel="stylesheet" href="../css/style.css" />
<html lang="is">
  <head>
    <meta charset="UTF-8" />
    <title>Kort</title>
    <style>
      #map {
        height: 80%; /* hæð kortsins */
        width: 100%; /* breidd kortsins */
      }
    </style>
  </head>
  <body>
    <h2>Staðsetning</h2>

    <iframe
      id="map"
      src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d13999.512121212!2d-21.933!3d64.135!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48d60a0e1234567%3A0xabcd1234abcd!2sReykjavík!5e0!3m2!1sis!2sis!4v1699999999999!5m2!1sis!2sis"
      width="600"
      height="450"
      style="border: 0"
      allowfullscreen=""
      loading="lazy"
      referrerpolicy="no-referrer-when-downgrade"
    >
    </iframe>
    <div class="fimmkassar">
      <a href="kort.html">
        <img src="../myndir/kort mynd.png" alt="Kort" />
      </a>
      <a href="samanburður.html">
        <img src="../myndir/berasamann.png" alt="Samanburður" />
      </a>
      <a href="forsiða.html">
        <img src="../myndir/borða.png" alt="Skanna" />
      </a>
      <a href="user.html">
        <img src="../myndir/user.png" alt="Notandi" />
      </a>
      <a href="bætaviðvoru.html">
        <img src="../myndir/plus.png" alt="Bæta við vöru" />
      </a>
    </div>
    <script>
      (function () {
        const current = decodeURI(
          location.pathname.split("/").pop() || "index.html"
        );
        document.querySelectorAll(".fimmkassar a[href]").forEach((a) => {
          const target = decodeURI(
            new URL(a.getAttribute("href"), location.href).pathname
              .split("/")
              .pop()
          );
          if (target === current) a.classList.add("active");
        });
      })();
    </script>
  </div>
  </body>
</html>
