"use strict";

try {
  const mapEl = document.getElementById("map");
  if (mapEl) {
    const map = L.map("map").setView([51.11045456280866, 16.981246594679913], 13);

    L.tileLayer("http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", {
      minZoom: 6,
      maxZoom: 20,
      subdomains: ["mt0", "mt1", "mt2", "mt3"],
    }).addTo(map);

    L.marker([51.11045456280866, 16.981246594679913]).addTo(map);
  }
} catch (e) {
  console.error(e);
}
