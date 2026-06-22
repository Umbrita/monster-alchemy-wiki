document.addEventListener("DOMContentLoaded", function () {
  const el = document.getElementById("wiki-map")
  console.log("wiki-map:", !!el)
  console.log("Leaflet:", typeof L)
  console.log("markers:", window.__MAP_MARKERS__)

  if (!el || typeof L === "undefined") return

  const map = L.map("wiki-map", {
    crs: L.CRS.Simple,
    minZoom: -2,
    maxZoom: 3,
  })

  const bounds = [[0, 0], [2048, 2048]]
  L.imageOverlay("/assets/map/map.png", bounds).addTo(map)
  map.fitBounds(bounds)

  const markers = window.__MAP_MARKERS__ || []
  markers.forEach((m) => {
    L.marker([m.y, m.x]).addTo(map).bindPopup(
      `<a href="/locations/${m.slug}"><strong>${m.name}</strong></a>`
    )
  })
})