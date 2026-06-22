---
title: Map
---

<div id="map-iframe-container"></div>

<script>
  window.addEventListener("DOMContentLoaded", function () {
    const iframe = document.createElement("iframe");
    iframe.src = "/static/map-raw";
    iframe.width = "100%";
    iframe.height = "550";
    iframe.style.border = "none";
    iframe.style.borderRadius = "8px";
    document.getElementById("map-iframe-container").appendChild(iframe);
  });
</script>