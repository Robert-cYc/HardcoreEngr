/**
 * Fancy Canvas Wave Engine
 * Features:
 *  - 5 layered sinusoidal waves with independent phase, speed, amplitude
 *  - Each wave rendered as a gradient-filled path
 *  - Hue-rotating color palette synchronized over time
 *  - Bright glowing crest line on the top wave
 *  - Floating sparkle particles that ride wave surfaces
 *  - Fully responsive (ResizeObserver)
 *  - Respects prefers-reduced-motion
 */
(function () {
  'use strict';

  const canvas = document.getElementById('wave-canvas');
  if (!canvas) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const ctx = canvas.getContext('2d');

  /* ── helpers ─────────────────────────────────────────────── */
  function isDark() {
    return (
      document.documentElement.classList.contains('dark-mode') ||
      document.body.classList.contains('dark-mode')
    );
  }

  function hsl(h, s, l, a) {
    a = (a === undefined) ? 1 : a;
    return 'hsla(' + (h % 360) + ',' + s + '%,' + l + '%,' + a + ')';
  }

  /* ── wave layer definitions ──────────────────────────────── */
  var WAVES = [
    { speed: 0.0008, amplitude: 14, frequency: 1.8, phaseOffset: 0,    yBase: 0.55, opacityScale: 0.85, hueOffset: 0   },
    { speed: 0.0013, amplitude: 10, frequency: 2.3, phaseOffset: 1.1,  yBase: 0.60, opacityScale: 0.65, hueOffset: 30  },
    { speed: 0.0006, amplitude: 18, frequency: 1.5, phaseOffset: 2.4,  yBase: 0.65, opacityScale: 0.50, hueOffset: 60  },
    { speed: 0.0018, amplitude:  8, frequency: 2.8, phaseOffset: 0.7,  yBase: 0.70, opacityScale: 0.35, hueOffset: 100 },
    { speed: 0.0010, amplitude: 22, frequency: 1.2, phaseOffset: 3.5,  yBase: 0.75, opacityScale: 0.22, hueOffset: 150 },
  ];

  /* ── sparkle particles ───────────────────────────────────── */
  var NUM_SPARKS = 28;
  var sparks = [];
  for (var i = 0; i < NUM_SPARKS; i++) {
    sparks.push({
      x: Math.random(),
      waveIndex: Math.floor(Math.random() * WAVES.length),
      size: 1 + Math.random() * 2.5,
      speedX: (0.00015 + Math.random() * 0.0003) * (Math.random() < 0.5 ? 1 : -1),
      opacity: 0.4 + Math.random() * 0.6,
      opacityDir: Math.random() < 0.5 ? 1 : -1,
      opacitySpeed: 0.005 + Math.random() * 0.01,
      hueOffset: Math.random() * 360,
    });
  }

  /* ── resize ──────────────────────────────────────────────── */
  function resize() {
    var rect = canvas.parentElement.getBoundingClientRect();
    canvas.width  = rect.width  * devicePixelRatio;
    canvas.height = rect.height * devicePixelRatio;
    canvas.style.width  = rect.width  + 'px';
    canvas.style.height = rect.height + 'px';
  }

  if (window.ResizeObserver) {
    new ResizeObserver(resize).observe(canvas.parentElement);
  } else {
    window.addEventListener('resize', resize);
  }
  resize();

  /* ── wave y-value at x ───────────────────────────────────── */
  function waveY(wave, x, t, H) {
    var phase = t * wave.speed + wave.phaseOffset;
    return wave.yBase * H + Math.sin(x * wave.frequency * Math.PI * 2 + phase) * wave.amplitude;
  }

  /* ── draw one wave layer ─────────────────────────────────── */
  function drawWave(wave, t, baseHue, dark) {
    var W = canvas.width;
    var H = canvas.height;
    var hue = (baseHue + wave.hueOffset) % 360;
    var opacity = (dark ? 0.32 : 0.20) * wave.opacityScale;
    var steps = Math.ceil(W / 4);

    var grad = ctx.createLinearGradient(0, 0, W, 0);
    grad.addColorStop(0,   hsl(hue,        80, dark ? 65 : 50, opacity));
    grad.addColorStop(0.4, hsl(hue + 40,   85, dark ? 70 : 55, opacity * 1.15));
    grad.addColorStop(0.7, hsl(hue + 80,   75, dark ? 60 : 45, opacity * 0.9));
    grad.addColorStop(1,   hsl(hue + 120,  80, dark ? 65 : 50, opacity));

    ctx.beginPath();
    ctx.moveTo(0, H);
    for (var i = 0; i <= steps; i++) {
      var x  = (i / steps) * W;
      var nx = i / steps;
      var y  = waveY(wave, nx, t, H);
      ctx.lineTo(x, y);
    }
    ctx.lineTo(W, H);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();
  }

  /* ── draw glowing crest on topmost wave ─────────────────── */
  function drawCrest(wave, t, baseHue, dark) {
    var W = canvas.width;
    var H = canvas.height;
    var hue = baseHue % 360;
    var steps = Math.ceil(W / 4);

    ctx.beginPath();
    for (var i = 0; i <= steps; i++) {
      var x  = (i / steps) * W;
      var nx = i / steps;
      var y  = waveY(wave, nx, t, H);
      if (i === 0) ctx.moveTo(x, y);
      else         ctx.lineTo(x, y);
    }
    ctx.strokeStyle = hsl(hue, 90, dark ? 80 : 65, 0.55);
    ctx.lineWidth   = 1.5 * devicePixelRatio;
    ctx.shadowColor = hsl(hue, 100, 70, 0.8);
    ctx.shadowBlur  = 8 * devicePixelRatio;
    ctx.stroke();
    ctx.shadowBlur  = 0;
    ctx.lineWidth   = 1;
  }

  /* ── update sparkle state ────────────────────────────────── */
  function updateSparks() {
    sparks.forEach(function(sp) {
      sp.x += sp.speedX;
      if (sp.x > 1) sp.x = 0;
      if (sp.x < 0) sp.x = 1;

      sp.opacity += sp.opacityDir * sp.opacitySpeed;
      if (sp.opacity > 1)   { sp.opacity = 1;   sp.opacityDir = -1; }
      if (sp.opacity < 0.2) { sp.opacity = 0.2; sp.opacityDir =  1; }
    });
  }

  /* ── draw sparkles ───────────────────────────────────────── */
  function drawSparks(t, baseHue, dark) {
    var W = canvas.width;
    var H = canvas.height;

    sparks.forEach(function(sp) {
      var wave = WAVES[sp.waveIndex];
      var y = waveY(wave, sp.x, t, H) - sp.size * 2;

      var hue = (baseHue + sp.hueOffset) % 360;
      var grd = ctx.createRadialGradient(
        sp.x * W, y, 0,
        sp.x * W, y, sp.size * 3
      );
      grd.addColorStop(0,   hsl(hue, 100, 90,  sp.opacity));
      grd.addColorStop(0.5, hsl(hue,  90, 70,  sp.opacity * 0.5));
      grd.addColorStop(1,   hsl(hue,  80, 60,  0));

      ctx.beginPath();
      ctx.arc(sp.x * W, y, sp.size * 3, 0, Math.PI * 2);
      ctx.fillStyle = grd;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(sp.x * W, y, sp.size * 0.6, 0, Math.PI * 2);
      ctx.fillStyle = hsl(hue, 100, 95, sp.opacity);
      ctx.fill();
    });
  }

  /* ── main loop ───────────────────────────────────────────── */
  var lastT = null;
  var elapsed = 0;

  function frame(now) {
    if (lastT === null) lastT = now;
    var dt = now - lastT;
    lastT = now;
    elapsed += dt;

    var dark    = isDark();
    var baseHue = (elapsed * 0.012) % 360;
    var W = canvas.width;
    var H = canvas.height;

    ctx.clearRect(0, 0, W, H);

    for (var i = WAVES.length - 1; i >= 0; i--) {
      drawWave(WAVES[i], elapsed, baseHue, dark);
    }

    drawCrest(WAVES[0], elapsed, baseHue, dark);

    updateSparks();
    drawSparks(elapsed, baseHue, dark);

    requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
})();
