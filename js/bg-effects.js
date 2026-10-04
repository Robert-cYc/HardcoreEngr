/**
 * Background Effects Switcher
 * Effects: Waver, Matrix, Net, Swarm, Life, Hex, DNA
 */
(function() {
  'use strict';
  
  const nav = document.querySelector('.nav');
  if (!nav) return;
  
  const toggleBtn = document.createElement('button');
  toggleBtn.className = 'theme-toggle';
  toggleBtn.style.marginLeft = '8px';
  toggleBtn.title = '切換背景特效 (Background Effects)';
  toggleBtn.setAttribute('aria-label', '切換背景特效');
  toggleBtn.textContent = '🪄';
  nav.appendChild(toggleBtn);
  
  const effects = ['waver', 'matrix', 'net', 'swarm', 'life', 'hex', 'dna', 'firework'];
  let currentIdx = localStorage.getItem('bg-effect-idx') ? parseInt(localStorage.getItem('bg-effect-idx')) : 0;
  // Ensure valid index if we added new effects
  if(currentIdx >= effects.length) currentIdx = 0;
  
  window.activeBgEffect = effects[currentIdx];
  
  const wavesContainer = document.querySelector('.waves');
  if (!wavesContainer) return;
  
  // Helper to create canvas
  function createCanvas(id, opacity) {
    const c = document.createElement('canvas');
    c.id = id;
    c.style.position = 'absolute';
    c.style.top = '0';
    c.style.left = '0';
    c.style.width = '100%';
    c.style.height = '100%';
    c.style.zIndex = '-1';
    c.style.opacity = opacity;
    c.style.display = 'none';
    wavesContainer.appendChild(c);
    return c;
  }
  
  const matrixCanvas = createCanvas('matrix-canvas', '0.4');
  const netCanvas = createCanvas('net-canvas', '0.7');
  const swarmCanvas = createCanvas('swarm-canvas', '0.8');
  const lifeCanvas = createCanvas('life-canvas', '0.6');
  const hexCanvas = createCanvas('hex-canvas', '0.9');
  const dnaCanvas = createCanvas('dna-canvas', '0.7');
  const fireworkCanvas = createCanvas('firework-canvas', '0.9');
  
  const waveCanvas = document.getElementById('wave-canvas');
  
  function applyEffect(idx) {
    currentIdx = idx;
    localStorage.setItem('bg-effect-idx', currentIdx);
    window.activeBgEffect = effects[currentIdx];
    
    if (waveCanvas) waveCanvas.style.display = window.activeBgEffect === 'waver' ? 'block' : 'none';
    matrixCanvas.style.display = window.activeBgEffect === 'matrix' ? 'block' : 'none';
    netCanvas.style.display = window.activeBgEffect === 'net' ? 'block' : 'none';
    swarmCanvas.style.display = window.activeBgEffect === 'swarm' ? 'block' : 'none';
    lifeCanvas.style.display = window.activeBgEffect === 'life' ? 'block' : 'none';
    hexCanvas.style.display = window.activeBgEffect === 'hex' ? 'block' : 'none';
    dnaCanvas.style.display = window.activeBgEffect === 'dna' ? 'block' : 'none';
    fireworkCanvas.style.display = window.activeBgEffect === 'firework' ? 'block' : 'none';
    
    if (window.activeBgEffect === 'matrix') initMatrix();
    if (window.activeBgEffect === 'net') initNet();
    if (window.activeBgEffect === 'swarm') initSwarm();
    if (window.activeBgEffect === 'life') initLife();
    if (window.activeBgEffect === 'hex') initHex();
    if (window.activeBgEffect === 'dna') initDNA();
    if (window.activeBgEffect === 'firework') initFirework();
  }
  
  toggleBtn.addEventListener('click', () => {
    applyEffect((currentIdx + 1) % effects.length);
  });
  
  // Track mouse globally for interactable canvases
  let mouseX = -1000, mouseY = -1000;
  const hoverEl = document.querySelector('.site-header') || wavesContainer;
  hoverEl.addEventListener('mousemove', (e) => {
    const rect = wavesContainer.getBoundingClientRect();
    mouseX = (e.clientX - rect.left) * window.devicePixelRatio;
    mouseY = (e.clientY - rect.top) * window.devicePixelRatio;
  });
  hoverEl.addEventListener('mouseleave', () => { mouseX = -1000; mouseY = -1000; });
  
  /* ================== MATRIX ================== */
  let matrixInterval;
  function initMatrix() {
    clearInterval(matrixInterval);
    const ctx = matrixCanvas.getContext('2d');
    const width = matrixCanvas.width = wavesContainer.clientWidth * window.devicePixelRatio;
    const height = matrixCanvas.height = wavesContainer.clientHeight * window.devicePixelRatio;
    const fontSize = 16 * window.devicePixelRatio;
    const columns = Math.floor(width / fontSize);
    const drops = [];
    for(let x = 0; x < columns; x++) drops[x] = 1;
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ".split('');
    
    matrixInterval = setInterval(() => {
      if (window.activeBgEffect !== 'matrix') return;
      const isDark = document.documentElement.classList.contains('dark-mode');
      ctx.fillStyle = isDark ? 'rgba(0, 0, 0, 0.1)' : 'rgba(255, 255, 255, 0.1)';
      ctx.fillRect(0, 0, width, height);
      ctx.fillStyle = isDark ? '#0F0' : '#0a0';
      ctx.font = fontSize + 'px monospace';
      for(let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        if(drops[i] * fontSize > height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
      }
    }, 82);
  }
  
  /* ================== NET ================== */
  let netAnim;
  function initNet() {
    cancelAnimationFrame(netAnim);
    const ctx = netCanvas.getContext('2d');
    const width = netCanvas.width = wavesContainer.clientWidth * window.devicePixelRatio;
    const height = netCanvas.height = wavesContainer.clientHeight * window.devicePixelRatio;
    const particles = [];
    const numParticles = Math.floor(((width * height) / 12000) * 1.3);
    const palettes = {
      dark: ['96, 165, 250', '52, 211, 153', '244, 114, 182', '167, 139, 250', '250, 204, 21'],
      light: ['37, 99, 235', '5, 150, 105', '219, 39, 119', '124, 58, 237', '217, 119, 6']
    };
    for(let i=0; i<numParticles; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 1.5,
        vy: (Math.random() - 0.5) * 1.5,
        radius: Math.random() * 2 + 1.5,
        colorIdx: Math.floor(Math.random() * 5)
      });
    }
    function draw() {
      if (window.activeBgEffect !== 'net') return;
      ctx.clearRect(0, 0, width, height);
      const isDark = document.documentElement.classList.contains('dark-mode');
      const currentPalette = isDark ? palettes.dark : palettes.light;
      for(let i=0; i<particles.length; i++) {
        const p = particles[i];
        p.x += p.vx; p.y += p.vy;
        if(p.x < 0 || p.x > width) p.vx *= -1;
        if(p.y < 0 || p.y > height) p.vy *= -1;
        const pColor = currentPalette[p.colorIdx];
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${pColor}, 0.8)`;
        ctx.fill();
        for(let j=i+1; j<particles.length; j++) {
          const p2 = particles[j];
          const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
          if(dist > 0 && dist < 150) {
            const opacity = 1 - dist/150;
            const p2Color = currentPalette[p2.colorIdx];
            const grad = ctx.createLinearGradient(p.x, p.y, p2.x, p2.y);
            grad.addColorStop(0, `rgba(${pColor}, ${opacity})`);
            grad.addColorStop(1, `rgba(${p2Color}, ${opacity})`);
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = grad;
            ctx.lineWidth = 1.5;
            ctx.stroke();
          }
        }
      }
      netAnim = requestAnimationFrame(draw);
    }
    draw();
  }
  
  /* ================== SWARM ================== */
  let swarmAnim;
  function initSwarm() {
    cancelAnimationFrame(swarmAnim);
    const ctx = swarmCanvas.getContext('2d');
    const width = swarmCanvas.width = wavesContainer.clientWidth * window.devicePixelRatio;
    const height = swarmCanvas.height = wavesContainer.clientHeight * window.devicePixelRatio;
    
    const boids = [];
    const numBoids = Math.floor((width * height) / 10000);
    for (let i = 0; i < numBoids; i++) {
      boids.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: Math.random() * 2 - 1,
        vy: Math.random() * 2 - 1
      });
    }

    function draw() {
      if (window.activeBgEffect !== 'swarm') return;
      ctx.clearRect(0, 0, width, height);
      const isDark = document.documentElement.classList.contains('dark-mode');
      ctx.fillStyle = isDark ? 'rgba(52, 211, 153, 0.8)' : 'rgba(5, 150, 105, 0.8)';

      for (let b of boids) {
        let cx = 0, cy = 0, avgVx = 0, avgVy = 0, count = 0;
        let sepX = 0, sepY = 0;
        
        for (let other of boids) {
          if (b === other) continue;
          let dx = b.x - other.x;
          let dy = b.y - other.y;
          let distSq = dx*dx + dy*dy;
          if (distSq < 4000) { 
            cx += other.x; cy += other.y;
            avgVx += other.vx; avgVy += other.vy;
            count++;
            if (distSq < 400) { 
              sepX += dx; sepY += dy;
            }
          }
        }
        
        if (count > 0) {
          cx /= count; cy /= count;
          avgVx /= count; avgVy /= count;
          b.vx += (cx - b.x) * 0.0005 + avgVx * 0.01 + sepX * 0.05;
          b.vy += (cy - b.y) * 0.0005 + avgVy * 0.01 + sepY * 0.05;
        }

        let mdx = b.x - mouseX;
        let mdy = b.y - mouseY;
        if (mdx*mdx + mdy*mdy < 15000) {
          b.vx += mdx * 0.002;
          b.vy += mdy * 0.002;
        }

        let speed = Math.sqrt(b.vx*b.vx + b.vy*b.vy);
        if (speed > 2) { b.vx = (b.vx/speed)*2; b.vy = (b.vy/speed)*2; }

        b.x += b.vx; b.y += b.vy;
        if (b.x < 0) b.x += width; if (b.x > width) b.x -= width;
        if (b.y < 0) b.y += height; if (b.y > height) b.y -= height;

        let angle = Math.atan2(b.vy, b.vx);
        let s = 1.5 * window.devicePixelRatio;
        ctx.save();
        ctx.translate(b.x, b.y);
        ctx.rotate(angle);
        ctx.beginPath();
        ctx.moveTo(8 * s, 0);
        ctx.lineTo(-4 * s, 4 * s);
        ctx.lineTo(-4 * s, -4 * s);
        ctx.fill();
        ctx.restore();
      }
      swarmAnim = requestAnimationFrame(draw);
    }
    draw();
  }
  
  /* ================== LIFE ================== */
  let lifeInterval;
  function initLife() {
    clearInterval(lifeInterval);
    const ctx = lifeCanvas.getContext('2d');
    const width = lifeCanvas.width = wavesContainer.clientWidth * window.devicePixelRatio;
    const height = lifeCanvas.height = wavesContainer.clientHeight * window.devicePixelRatio;
    const cellSize = 12 * window.devicePixelRatio;
    const cols = Math.floor(width / cellSize);
    const rows = Math.floor(height / cellSize);
    
    let grid = new Array(cols).fill(0).map(() => new Array(rows).fill(0).map(() => Math.random() > 0.85 ? 1 : 0));
    
    lifeInterval = setInterval(() => {
      if (window.activeBgEffect !== 'life') return;
      const isDark = document.documentElement.classList.contains('dark-mode');
      ctx.fillStyle = isDark ? 'rgba(0,0,0,0.15)' : 'rgba(255,255,255,0.15)';
      ctx.fillRect(0, 0, width, height);
      
      ctx.fillStyle = isDark ? 'rgba(96, 165, 250, 0.6)' : 'rgba(37, 99, 235, 0.6)';
      
      let newGrid = new Array(cols).fill(0).map(() => new Array(rows).fill(0));
      let aliveCount = 0;
      for (let x = 0; x < cols; x++) {
        for (let y = 0; y < rows; y++) {
          let neighbors = 0;
          for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
              if (i === 0 && j === 0) continue;
              let nx = (x + i + cols) % cols;
              let ny = (y + j + rows) % rows;
              neighbors += grid[nx][ny];
            }
          }
          if (grid[x][y] === 1 && (neighbors === 2 || neighbors === 3)) newGrid[x][y] = 1;
          else if (grid[x][y] === 0 && neighbors === 3) newGrid[x][y] = 1;
          else newGrid[x][y] = 0;
          
          if (newGrid[x][y] === 1) {
            ctx.fillRect(x * cellSize, y * cellSize, cellSize - 1, cellSize - 1);
            aliveCount++;
          }
        }
      }
      grid = newGrid;
      if (aliveCount < cols * rows * 0.02) {
         for(let i=0; i<10; i++) {
           grid[Math.floor(Math.random()*cols)][Math.floor(Math.random()*rows)] = 1;
         }
      }
    }, 100);
  }
  
  /* ================== HEX ================== */
  let hexAnim;
  function initHex() {
    cancelAnimationFrame(hexAnim);
    const ctx = hexCanvas.getContext('2d');
    const width = hexCanvas.width = wavesContainer.clientWidth * window.devicePixelRatio;
    const height = hexCanvas.height = wavesContainer.clientHeight * window.devicePixelRatio;
    
    const size = 15 * window.devicePixelRatio;
    const hexWidth = Math.sqrt(3) * size;
    const hexHeight = 2 * size;
    const cols = Math.ceil(width / hexWidth) + 1;
    const rows = Math.ceil(height / (hexHeight * 0.75)) + 1;
    
    const hexes = [];
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        let x = col * hexWidth;
        if (row % 2 !== 0) x += hexWidth / 2;
        let y = row * hexHeight * 0.75;
        hexes.push({x, y, glow: 0});
      }
    }
    
    // Add cyber bees!
    const numBees = 5;
    const bees = [];
    for(let i=0; i<numBees; i++) {
      bees.push({
        x: Math.random() * width,
        y: Math.random() * height,
        angle: Math.random() * Math.PI * 2
      });
    }

    function drawHex(x, y, s) {
      ctx.beginPath();
      for (let i = 0; i < 6; i++) {
        let angle = Math.PI / 180 * (60 * i - 30);
        let hx = x + s * Math.cos(angle);
        let hy = y + s * Math.sin(angle);
        if (i === 0) ctx.moveTo(hx, hy);
        else ctx.lineTo(hx, hy);
      }
      ctx.closePath();
    }

    let time = 0;
    function draw() {
      if (window.activeBgEffect !== 'hex') return;
      ctx.clearRect(0, 0, width, height);
      const isDark = document.documentElement.classList.contains('dark-mode');
      time += 0.5;
      
      // Update bees
      for(let b of bees) {
        b.angle += (Math.random() - 0.5) * 0.5; // Wander randomly
        b.x += Math.cos(b.angle) * 2;
        b.y += Math.sin(b.angle) * 2;
        
        // Wrap around screen
        if (b.x < -20) b.x = width + 20;
        if (b.x > width + 20) b.x = -20;
        if (b.y < -20) b.y = height + 20;
        if (b.y > height + 20) b.y = -20;
      }
      
      for (let h of hexes) {
        let dx = h.x - mouseX;
        let dy = h.y - mouseY;
        if (dx*dx + dy*dy < 20000) h.glow = 1;
        
        // Bees also trigger hex glow!
        for (let b of bees) {
          let bdx = h.x - b.x;
          let bdy = h.y - b.y;
          if (bdx*bdx + bdy*bdy < 5000) h.glow = Math.max(h.glow, 0.8);
        }
        
        if (h.glow > 0) h.glow -= 0.015;
        
        drawHex(h.x, h.y, size * 0.95);
        if (h.glow > 0) {
          // Constantly changing colors based on time and position
          let hue = (time + h.x * 0.1 + h.y * 0.1) % 360;
          let lightness = isDark ? 65 : 45;
          ctx.strokeStyle = `hsla(${hue}, 80%, ${lightness}%, ${h.glow})`;
          ctx.lineWidth = 2 * window.devicePixelRatio;
          ctx.stroke();
          ctx.fillStyle = `hsla(${hue}, 80%, ${lightness}%, ${h.glow * 0.2})`;
          ctx.fill();
        } else {
          ctx.strokeStyle = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }
      
      // Draw bees
      for(let b of bees) {
        ctx.save();
        ctx.translate(b.x, b.y);
        ctx.rotate(b.angle);
        ctx.scale(1.5, 1.5); // Enlarge bee by 50%
        
        // Bee glow / shadow
        ctx.shadowColor = '#f59e0b';
        ctx.shadowBlur = 10;
        
        // Bee body (yellow/orange ellipse)
        ctx.fillStyle = '#fbbf24';
        ctx.beginPath();
        ctx.ellipse(0, 0, 5, 3, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Bee wings (flapping based on time)
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.shadowBlur = 0;
        let flap = Math.sin(time * 2) * (Math.PI / 4);
        
        ctx.beginPath();
        ctx.ellipse(0, -3, 3, 4, flap, 0, Math.PI * 2); // Left wing
        ctx.fill();
        
        ctx.beginPath();
        ctx.ellipse(0, 3, 3, 4, -flap, 0, Math.PI * 2); // Right wing
        ctx.fill();
        
        ctx.restore();
      }
      
      hexAnim = requestAnimationFrame(draw);
    }
    draw();
  }
  
  /* ================== DNA ================== */
  let dnaAnim;
  function initDNA() {
    cancelAnimationFrame(dnaAnim);
    const ctx = dnaCanvas.getContext('2d');
    const width = dnaCanvas.width = wavesContainer.clientWidth * window.devicePixelRatio;
    const height = dnaCanvas.height = wavesContainer.clientHeight * window.devicePixelRatio;
    
    let time = 0;
    const pCount = Math.floor(width / 10);
    const chars = ['0', '1'];
    
    function draw() {
      if (window.activeBgEffect !== 'dna') return;
      ctx.clearRect(0, 0, width, height);
      const isDark = document.documentElement.classList.contains('dark-mode');
      const color1 = isDark ? '96, 165, 250' : '37, 99, 235';
      const color2 = isDark ? '52, 211, 153' : '5, 150, 105';
      
      time += 0.015;
      
      for (let i = 0; i < pCount; i++) {
        let x = (i / pCount) * width;
        let angle = i * 0.1 + time;
        let yOffset = Math.cos(angle) * (height * 0.25);
        let z1 = Math.sin(angle);
        
        let y1 = height/2 + yOffset;
        let y2 = height/2 - yOffset;
        
        ctx.beginPath();
        ctx.moveTo(x, y1);
        ctx.lineTo(x, y2);
        ctx.strokeStyle = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
        ctx.stroke();
        
        let s1 = (z1 + 2) * 5 * window.devicePixelRatio;
        ctx.font = `${s1}px monospace`;
        ctx.fillStyle = `rgba(${color1}, ${0.4 + (z1+1)*0.3})`;
        ctx.fillText(chars[i%2], x - s1/2, y1 + s1/2);
        
        let z2 = Math.sin(angle + Math.PI);
        let s2 = (z2 + 2) * 5 * window.devicePixelRatio;
        ctx.font = `${s2}px monospace`;
        ctx.fillStyle = `rgba(${color2}, ${0.4 + (z2+1)*0.3})`;
        ctx.fillText(chars[(i+1)%2], x - s2/2, y2 + s2/2);
      }
      dnaAnim = requestAnimationFrame(draw);
    }
    draw();
  }

  /* ================== FIREWORK ================== */
  let fireworkAnim;
  function initFirework() {
    cancelAnimationFrame(fireworkAnim);
    const ctx = fireworkCanvas.getContext('2d');
    const width = fireworkCanvas.width = wavesContainer.clientWidth * window.devicePixelRatio;
    const height = fireworkCanvas.height = wavesContainer.clientHeight * window.devicePixelRatio;
    
    let fireworks = [];
    let particles = [];
    
    function createFirework() {
      const x = Math.random() * width;
      const y = height;
      const targetY = Math.random() * (height / 2);
      const speed = Math.random() * 3 + 4;
      const angle = Math.PI / 2 + (Math.random() - 0.5) * 0.5;
      const vx = Math.cos(angle) * speed;
      const vy = -Math.sin(angle) * speed;
      const hue = Math.floor(Math.random() * 360);
      fireworks.push({ x, y, targetY, vx, vy, hue });
    }
    
    function explode(x, y, hue) {
      const particleCount = 60 + Math.random() * 40;
      for (let i = 0; i < particleCount; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 4 + 1;
        particles.push({
          x: x,
          y: y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          alpha: 1,
          hue: hue + (Math.random() - 0.5) * 30,
          size: Math.random() * 2 + 1,
          decay: Math.random() * 0.015 + 0.015
        });
      }
    }
    
    function draw() {
      if (window.activeBgEffect !== 'firework') return;
      
      const isDark = document.documentElement.classList.contains('dark-mode');
      ctx.fillStyle = isDark ? 'rgba(15, 23, 42, 0.2)' : 'rgba(255, 255, 255, 0.2)';
      ctx.fillRect(0, 0, width, height);
      
      if (Math.random() < 0.04) {
        createFirework();
      }
      
      for (let i = fireworks.length - 1; i >= 0; i--) {
        let f = fireworks[i];
        f.x += f.vx;
        f.y += f.vy;
        f.vy += 0.05; // gravity
        
        ctx.beginPath();
        ctx.arc(f.x, f.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = `hsl(${f.hue}, 100%, 60%)`;
        ctx.fill();
        
        if (f.vy >= 0 || f.y <= f.targetY) {
          explode(f.x, f.y, f.hue);
          fireworks.splice(i, 1);
        }
      }
      
      for (let i = particles.length - 1; i >= 0; i--) {
        let p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.03; // gravity
        p.alpha -= p.decay;
        
        if (p.alpha <= 0) {
          particles.splice(i, 1);
          continue;
        }
        
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${p.hue}, 100%, 60%, ${p.alpha})`;
        ctx.fill();
      }
      
      fireworkAnim = requestAnimationFrame(draw);
    }
    draw();
  }
  
  // Re-init current effect on resize
  window.addEventListener('resize', () => {
    if (window.activeBgEffect === 'matrix') initMatrix();
    if (window.activeBgEffect === 'net') initNet();
    if (window.activeBgEffect === 'swarm') initSwarm();
    if (window.activeBgEffect === 'life') initLife();
    if (window.activeBgEffect === 'hex') initHex();
    if (window.activeBgEffect === 'dna') initDNA();
    if (window.activeBgEffect === 'firework') initFirework();
  });
  
  // Init on load
  applyEffect(currentIdx);
  
})();
