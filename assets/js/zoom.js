/* Image zoom, powered by the vendored medium-zoom build in
   assets/js/lib/medium-zoom.min.js. Enabled by params.image_zoom. */
(function () {
  if (typeof mediumZoom !== 'function') return;

  var opts = window.poisonZoom || {};
  mediumZoom('.zoomable', {
    background: opts.background || 'rgba(0, 0, 0, 0.9)',
    margin: typeof opts.margin === 'number' ? opts.margin : 20
  });
})();
