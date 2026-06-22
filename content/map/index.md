---
title: Map
---

<div id="map-iframe-container"></div>

<script>
  window.addEventListener("DOMContentLoaded", function () {
    const iframe = document.createElement("iframe");
    const isLocal =
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1";

    iframe.src = isLocal
      ? "/static/map-raw"
      : "/monster-alchemy-wiki/static/map-raw";

    iframe.width = "100%";
    iframe.height = "550";
    iframe.style.border = "none";
    iframe.style.borderRadius = "8px";
    iframe.allowFullscreen = true;
    iframe.setAttribute("allow", "fullscreen");

    document.getElementById("map-iframe-container").appendChild(iframe);
  });
</script>