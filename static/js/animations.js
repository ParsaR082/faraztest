/**
 * GSAP animations: reveals, counters, anatomy 3D, FAQ, hero magnetic button
 */
(function () {
  let anatomyReady = false;
  const isTouch = window.matchMedia('(pointer: coarse)').matches;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const LAYER_DEPTHS = { '1': 250, '2': 100, '3': -50, '4': -200 };

  const initAnatomy = () => {
    if (anatomyReady || typeof gsap === 'undefined') return;
    const anatomySec = document.getElementById('anatomy');
    const scene = document.getElementById('scene-3d');
    const layers = scene ? Array.from(scene.querySelectorAll('.layer')) : [];
    if (!anatomySec || layers.length < 4 || window.innerWidth < 1024) return;

    anatomyReady = true;
    const mm = gsap.matchMedia();

    mm.add('(min-width: 1024px)', () => {
      const timeline = gsap.timeline({
        scrollTrigger: {
          trigger: anatomySec,
          start: 'top top',
          end: '+=700',
          scrub: true,
          pin: '#anatomy .sticky-wrapper',
          invalidateOnRefresh: true,
          anticipatePin: 1,
        },
      });

      layers.forEach((layer, index) => {
        const infoId = layer.getAttribute('data-info');
        const maxZ = LAYER_DEPTHS[infoId] ?? (parseFloat(layer.getAttribute('data-depth')) || 0);
        const spreadX = index % 2 === 0 ? 16 : -16;
        timeline.to(
          layer,
          { z: maxZ, x: spreadX, y: index * 8, ease: 'none', force3D: true },
          0
        );
      });
    });

    layers.forEach((layer) => {
      const infoId = layer.getAttribute('data-info');
      const infoBox = document.getElementById(`info-${infoId}`);
      if (!infoBox) return;

      const showInfo = () => {
        const rect = layer.getBoundingClientRect();
        const infoWidth = 300;
        let left = rect.left + rect.width + 40;
        let top = rect.top + rect.height / 2 - 70;
        if (left + infoWidth > window.innerWidth - 16) left = rect.left - infoWidth - 20;
        if (top < 16) top = 16;
        if (top + 160 > window.innerHeight - 16) top = window.innerHeight - 176;
        infoBox.style.left = `${left}px`;
        infoBox.style.top = `${top}px`;
        infoBox.classList.add('active');
      };

      layer.addEventListener('mouseenter', showInfo);
      layer.addEventListener('mouseleave', () => infoBox.classList.remove('active'));
      layer.addEventListener('click', () => {
        const isActive = infoBox.classList.contains('active');
        document.querySelectorAll('#anatomy .layer-info-2d').forEach((b) => b.classList.remove('active'));
        if (!isActive) showInfo();
      });
    });

    const closeTooltips = () => {
      anatomySec.querySelectorAll('.layer-info-2d').forEach((b) => b.classList.remove('active'));
    };
    window.addEventListener('scroll', closeTooltips, { passive: true });
    window.addEventListener('resize', closeTooltips);
  };

  const init = () => {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
      document.querySelectorAll('.reveal').forEach((el) => {
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
      document.querySelectorAll('.stat-num').forEach((el) => {
        const target = +el.dataset.count;
        if (target === 98) el.textContent = '98%';
        else if (target === 1200) el.textContent = '1200+';
        else if (target === 15) el.textContent = '15+';
        else if (target === 24) el.textContent = '24';
        else el.textContent = String(target);
      });
      return;
    }

    gsap.registerPlugin(ScrollTrigger);

    const magBtn = document.getElementById('mag-btn');
    if (magBtn && !isTouch && !reduced) {
      magBtn.addEventListener('mousemove', (e) => {
        const rect = magBtn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        magBtn.style.transform = `translate(${x * 0.18}px, ${y * 0.18}px)`;
      });
      magBtn.addEventListener('mouseleave', () => {
        magBtn.style.transform = 'translate(0, 0)';
      });
    }

    if (!reduced) {
      document.querySelectorAll('main section').forEach((section) => {
        const items = section.querySelectorAll('.reveal');
        if (!items.length) return;
        gsap.fromTo(
          items,
          { opacity: 0, y: 16 },
          {
            opacity: 1,
            y: 0,
            duration: 0.45,
            stagger: 0.06,
            ease: 'power2.out',
            scrollTrigger: {
              trigger: section,
              start: 'top 82%',
              toggleActions: 'play none none none',
            },
          }
        );
      });

      gsap.utils.toArray('.stat-num').forEach((el) => {
        const target = +el.dataset.count;
        const countObj = { value: 0 };
        gsap.to(countObj, {
          value: target,
          duration: 1.1,
          ease: 'power1.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            toggleActions: 'play none none none',
          },
          onUpdate: () => {
            const currentVal = Math.floor(countObj.value);
            if (target === 24) el.textContent = '24';
            else if (target === 98) el.textContent = `${currentVal}%`;
            else if (target === 1200) el.textContent = `${currentVal}+`;
            else if (target === 15) el.textContent = `${currentVal}+`;
            else el.textContent = String(currentVal);
          },
        });
      });
    } else {
      document.querySelectorAll('.reveal').forEach((el) => {
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
      document.querySelectorAll('.stat-num').forEach((el) => {
        const target = +el.dataset.count;
        if (target === 98) el.textContent = '98%';
        else if (target === 1200) el.textContent = '1200+';
        else if (target === 15) el.textContent = '15+';
        else el.textContent = String(target);
      });
    }

    const runAnatomy = () => {
      initAnatomy();
      ScrollTrigger.refresh();
    };

    if (document.fonts?.ready) {
      document.fonts.ready.then(runAnatomy);
    } else {
      runAnatomy();
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.addEventListener('load', () => {
    setTimeout(() => {
      if (typeof ScrollTrigger !== 'undefined') ScrollTrigger.refresh(true);
    }, 500);
  });
})();
