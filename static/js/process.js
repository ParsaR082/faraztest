/**
 * Process timeline + stat progress bars + mobile accordion
 */
(function () {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const fills = document.querySelectorAll('.stat-progress-fill');
  if (fills.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const fill = entry.target;
        const target = Math.min(100, Math.max(0, Number(fill.dataset.progress) || 0));
        fill.style.setProperty('--progress-target', `${target}%`);
        requestAnimationFrame(() => fill.classList.add('is-animated'));
        observer.unobserve(fill);
      });
    }, { threshold: 0.35 });
    fills.forEach((fill) => observer.observe(fill));
  }

  const board = document.getElementById('processBoard');
  if (board && !window.matchMedia('(max-width: 768px)').matches) {
    const path = board.querySelector('.process-connector-path');
    const nodes = board.querySelectorAll('.process-node-item');

    const activateNodes = (stagger) => {
      nodes.forEach((node, index) => {
        const delay = stagger && !reduced ? 180 + index * 160 : 0;
        setTimeout(() => node.classList.add('is-active'), delay);
      });
    };

    const animateConnector = () => {
      if (!path || typeof path.getTotalLength !== 'function') {
        activateNodes(!reduced);
        return;
      }
      const length = path.getTotalLength();
      path.style.strokeDasharray = `${length}`;
      path.style.strokeDashoffset = reduced ? '0' : `${length}`;
      if (!reduced) {
        requestAnimationFrame(() => {
          board.classList.add('is-visible');
          path.style.strokeDashoffset = '0';
        });
      } else {
        board.classList.add('is-visible');
      }
      activateNodes(!reduced);
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        animateConnector();
        observer.disconnect();
      });
    }, { threshold: 0.2 });
    observer.observe(board);
  }

  const accordion = document.getElementById('processAccordion');
  if (accordion) {
    accordion.querySelectorAll('.process-acc-item').forEach((item) => {
      item.addEventListener('toggle', () => {
        if (!item.open) return;
        accordion.querySelectorAll('.process-acc-item').forEach((other) => {
          if (other !== item) other.open = false;
        });
      });
    });
  }
})();
