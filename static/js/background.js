/**
 * Canvas particle background
 */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const init = () => {
    const canvas = document.getElementById('bg-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let w;
    let h;
    let particles = [];

    const initCanvas = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
      const count = w < 768 ? 16 : 32;
      particles = [];
      for (let i = 0; i < count; i++) {
        const isWater = Math.random() > 0.5;
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          isWater,
          size: Math.random() * (isWater ? 3 : 2.5) + 1,
          speedY: isWater ? Math.random() * 0.8 + 0.35 : -(Math.random() * 1.8 + 0.8),
          speedX: (Math.random() - 0.5) * 0.35,
          opacity: Math.random() * 0.4 + 0.08,
        });
      }
    };

    const drawParticles = () => {
      ctx.clearRect(0, 0, w, h);
      particles.forEach((p) => {
        p.y += p.speedY;
        p.x += p.speedX;
        if (p.y > h + 20 || p.y < -20 || p.x < -20 || p.x > w + 20) {
          p.x = Math.random() * w;
          p.y = p.isWater ? -10 : h + 10;
        }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = p.isWater
          ? `rgba(148, 163, 184, ${p.opacity})`
          : `rgba(255, 120, 78, ${p.opacity})`;
        ctx.fill();
      });
      requestAnimationFrame(drawParticles);
    };

    window.addEventListener('resize', initCanvas);
    initCanvas();
    drawParticles();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
