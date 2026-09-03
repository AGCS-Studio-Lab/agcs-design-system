// Fits an .agcs-canvas (3840x2160) to the viewport via transform: scale().
(function () {
  function fit() {
    var c = document.querySelector('.agcs-canvas');
    if (!c) return;
    var sx = window.innerWidth  / 3840;
    var sy = window.innerHeight / 2160;
    var s = Math.min(sx, sy);
    c.style.setProperty('--scale', s);
  }
  window.addEventListener('resize', fit);
  window.addEventListener('load', fit);
  fit();
})();
