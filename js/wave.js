/**
 * Fancy Canvas Wave Engine
 * Features:
 *  - 5 layered sinusoidal waves with independent phase, speed, amplitude
 *  - Each wave rendered as a gradient-filled path
 *  - Hue-rotating color palette synchronized over time
 *  - Bright glowing crest line on the top wave
 *  - Floating sparkle particles that ride wave surfaces
 *  - Interactive surface: pointer bulges the sea, click drops ripples
 *  - Data packets streaming along the glowing crest
 *  - Occasional shooting stars in dark mode
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

  /* ── data packets streaming along the crest ──────────────── */
  var NUM_PACKETS = 7;
  var packets = [];
  for (var pi = 0; pi < NUM_PACKETS; pi++) {
    packets.push({
      offset: Math.random(),
      speed: 0.02 + Math.random() * 0.03,
      size: 1.5 + Math.random() * 1.8,
      hueOffset: Math.random() * 360,
    });
  }

  /* ── shooting stars (dark mode only) ─────────────────────── */
  var stars = [];
  var nextStarAt = 2500;

  function spawnStar() {
    var dir = Math.random() < 0.5 ? 1 : -1;
    stars.push({
      x: 0.2 + Math.random() * 0.6,
      y: 0.08 + Math.random() * 0.3,
      vx: dir * (0.22 + Math.random() * 0.12),
      vy: 0.10 + Math.random() * 0.06,
      born: null,
      life: 700 + Math.random() * 500,
      hueOffset: Math.random() * 60,
    });
  }

  /* ── pointer interaction state ───────────────────────────── */
  var mouse = { x: 0.5, energy: 0, target: 0 };
  var ripples = [];
  var RIPPLE_LIFE = 1400;

  var hoverEl = document.querySelector('.site-header') || canvas.parentElement;
  hoverEl.addEventListener('pointermove', function (e) {
    var rect = canvas.getBoundingClientRect();
    mouse.x = Math.min(1.5, Math.max(-0.5, (e.clientX - rect.left) / rect.width));
    mouse.target = 1;
  });
  hoverEl.addEventListener('pointerleave', function () {
    mouse.target = 0;
  });
  hoverEl.addEventListener('pointerdown', function (e) {
    var rect = canvas.getBoundingClientRect();
    var nx = (e.clientX - rect.left) / rect.width;
    if (nx >= -0.05 && nx <= 1.05) {
      ripples.push({ x: nx, born: null });
      if (ripples.length > 6) ripples.shift();
    }
  });

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

  /* ── surface disturbance: pointer bulge + click ripples ──── */
  function perturb(nx) {
    var dy = 0;
    if (mouse.energy > 0.02) {
      var mdx = nx - mouse.x;
      dy -= Math.exp(-(mdx * mdx) / 0.004) * mouse.energy * 24;
    }
    for (var i = 0; i < ripples.length; i++) {
      var r = ripples[i];
      if (r.born === null) continue;
      var age = elapsed - r.born;
      if (age > RIPPLE_LIFE) continue;
      var dx = nx - r.x;
      var radius = (age / 1000) * 0.28;
      var band = Math.exp(-Math.pow((Math.abs(dx) - radius) * 16, 2));
      var decay = 1 - age / RIPPLE_LIFE;
      dy -= band * decay * 16 * Math.sin(age / 90);
    }
    return dy;
  }

  /* ── wave y-value at x ───────────────────────────────────── */
  function waveY(wave, x, t, H) {
    var phase = t * wave.speed + wave.phaseOffset;
    return wave.yBase * H + Math.sin(x * wave.frequency * Math.PI * 2 + phase) * wave.amplitude + perturb(x);
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

  /* ── draw packets riding the crest ───────────────────────── */
  function drawPackets(t, baseHue, dark) {
    var W = canvas.width;
    var H = canvas.height;
    var crest = WAVES[0];

    packets.forEach(function(pk) {
      var head = ((t * pk.speed + pk.offset) % 1 + 1) % 1;
      var hue = (baseHue + pk.hueOffset) % 360;

      for (var k = 1; k <= 4; k++) {
        var tailX = head - k * 0.012;
        if (tailX < 0) continue;
        var ty = waveY(crest, tailX, t, H) - pk.size * 2.2;
        ctx.beginPath();
        ctx.arc(tailX * W, ty, Math.max(0.3, pk.size * (1 - k * 0.18)), 0, Math.PI * 2);
        ctx.fillStyle = hsl(hue, 95, dark ? 75 : 60, 0.35 * (1 - k / 5));
        ctx.fill();
      }

      var hy = waveY(crest, head, t, H) - pk.size * 2.2;
      ctx.beginPath();
      ctx.arc(head * W, hy, pk.size * 0.55, 0, Math.PI * 2);
      ctx.fillStyle = hsl(hue, 100, 92, 0.95);
      ctx.fill();
    });
  }

  /* ── update & draw shooting stars ────────────────────────── */
  function updateStars(dark) {
    if (!dark) {
      stars.length = 0;
      return;
    }
    if (elapsed > nextStarAt && stars.length < 2) {
      spawnStar();
      nextStarAt = elapsed + 3500 + Math.random() * 5500;
    }

    var W = canvas.width;
    var H = canvas.height;

    for (var i = stars.length - 1; i >= 0; i--) {
      var s = stars[i];
      if (s.born === null) s.born = elapsed;
      var age = elapsed - s.born;
      if (age > s.life) {
        stars.splice(i, 1);
        continue;
      }
      var fade = Math.sin((age / s.life) * Math.PI);
      var x = (s.x + s.vx * (age / 1000)) * W;
      var y = (s.y + s.vy * (age / 1000)) * H;
      var ang = Math.atan2(s.vy * H, s.vx * W);
      var tailLen = 60 * devicePixelRatio * fade;
      var tx = x - Math.cos(ang) * tailLen;
      var ty = y - Math.sin(ang) * tailLen;

      var grad = ctx.createLinearGradient(tx, ty, x, y);
      grad.addColorStop(0, hsl(45 + s.hueOffset, 100, 85, 0));
      grad.addColorStop(1, hsl(45 + s.hueOffset, 100, 88, 0.9 * fade));
      ctx.strokeStyle = grad;
      ctx.lineWidth = 1.6 * devicePixelRatio;
      ctx.beginPath();
      ctx.moveTo(tx, ty);
      ctx.lineTo(x, y);
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(x, y, 1.6 * devicePixelRatio, 0, Math.PI * 2);
      ctx.fillStyle = hsl(48, 100, 96, fade);
      ctx.fill();
      ctx.lineWidth = 1;
    }
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

    /* interaction state easing */
    mouse.energy += (mouse.target - mouse.energy) * Math.min(1, dt * 0.006);
    for (var ri = ripples.length - 1; ri >= 0; ri--) {
      if (ripples[ri].born === null) { ripples[ri].born = elapsed; continue; }
      if (elapsed - ripples[ri].born > RIPPLE_LIFE) ripples.splice(ri, 1);
    }

    ctx.clearRect(0, 0, W, H);

    for (var i = WAVES.length - 1; i >= 0; i--) {
      drawWave(WAVES[i], elapsed, baseHue, dark);
    }

    drawCrest(WAVES[0], elapsed, baseHue, dark);

    updateSparks();
    drawSparks(elapsed, baseHue, dark);

    drawPackets(elapsed, baseHue, dark);
    updateStars(dark);

    requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
})();
