/**
 * Background Effects Switcher
 * Effects: Waver, Matrix, Net (Particle Constellation)
 */
(function() {
  'use strict';
  
  // 1. Inject the magic button
  const nav = document.querySelector('.nav');
  if (!nav) return;
  
  const toggleBtn = document.createElement('button');
  toggleBtn.className = 'theme-toggle';
  toggleBtn.style.marginLeft = '8px';
  toggleBtn.title = '切換背景特效 (Background Effects)';
  toggleBtn.setAttribute('aria-label', '切換背景特效');
  toggleBtn.textContent = '🪄';
  nav.appendChild(toggleBtn);
  
  const effects = ['waver', 'matrix', 'net'];
  let currentIdx = localStorage.getItem('bg-effect-idx') ? parseInt(localStorage.getItem('bg-effect-idx')) : 0;
  
  window.activeBgEffect = effects[currentIdx];
  
  // 2. Prepare containers
  const wavesContainer = document.querySelector('.waves');
  if (!wavesContainer) return;
  
  // Matrix Canvas
  const matrixCanvas = document.createElement('canvas');
  matrixCanvas.id = 'matrix-canvas';
  matrixCanvas.style.position = 'absolute';
  matrixCanvas.style.top = '0';
  matrixCanvas.style.left = '0';
  matrixCanvas.style.width = '100%';
  matrixCanvas.style.height = '100%';
  matrixCanvas.style.zIndex = '-1';
  matrixCanvas.style.opacity = '0.4';
  matrixCanvas.style.display = 'none';
  wavesContainer.appendChild(matrixCanvas);
  
  // Net Canvas
  const netCanvas = document.createElement('canvas');
  netCanvas.id = 'net-canvas';
  netCanvas.style.position = 'absolute';
  netCanvas.style.top = '0';
  netCanvas.style.left = '0';
  netCanvas.style.width = '100%';
  netCanvas.style.height = '100%';
  netCanvas.style.zIndex = '-1';
  netCanvas.style.opacity = '0.7';
  netCanvas.style.display = 'none';
  wavesContainer.appendChild(netCanvas);
  
  const waveCanvas = document.getElementById('wave-canvas');
  
  function applyEffect(idx) {
    currentIdx = idx;
    localStorage.setItem('bg-effect-idx', currentIdx);
    window.activeBgEffect = effects[currentIdx];
    
    if (waveCanvas) waveCanvas.style.display = window.activeBgEffect === 'waver' ? 'block' : 'none';
    matrixCanvas.style.display = window.activeBgEffect === 'matrix' ? 'block' : 'none';
    netCanvas.style.display = window.activeBgEffect === 'net' ? 'block' : 'none';
    
    // Trigger initial resizes
    if (window.activeBgEffect === 'matrix') initMatrix();
    if (window.activeBgEffect === 'net') initNet();
  }
  
  toggleBtn.addEventListener('click', () => {
    applyEffect((currentIdx + 1) % effects.length);
  });
  
  // --- Matrix Effect ---
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
    }, 33);
  }
  
  // --- Net (Particle Constellation) Effect ---
  let netAnim;
  function initNet() {
    cancelAnimationFrame(netAnim);
    const ctx = netCanvas.getContext('2d');
    const width = netCanvas.width = wavesContainer.clientWidth * window.devicePixelRatio;
    const height = netCanvas.height = wavesContainer.clientHeight * window.devicePixelRatio;
    
    const particles = [];
    const numParticles = Math.floor((width * height) / 30000); // Scale by area
    
    for(let i=0; i<numParticles; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 1.5,
        vy: (Math.random() - 0.5) * 1.5,
        radius: Math.random() * 2 + 1
      });
    }
    
    function draw() {
      if (window.activeBgEffect !== 'net') return;
      ctx.clearRect(0, 0, width, height);
      const isDark = document.documentElement.classList.contains('dark-mode');
      const color = isDark ? '255, 255, 255' : '0, 0, 0';
      
      for(let i=0; i<particles.length; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        
        if(p.x < 0 || p.x > width) p.vx *= -1;
        if(p.y < 0 || p.y > height) p.vy *= -1;
        
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${color}, 0.5)`;
        ctx.fill();
        
        for(let j=i+1; j<particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx*dx + dy*dy);
          
          if(dist < 150) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(${color}, ${1 - dist/150})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      }
      netAnim = requestAnimationFrame(draw);
    }
    draw();
  }
  
  window.addEventListener('resize', () => {
    if (window.activeBgEffect === 'matrix') initMatrix();
    if (window.activeBgEffect === 'net') initNet();
  });
  
  // Init on load
  applyEffect(currentIdx);
  
})();
