/**
 * Navigation, header scroll, mobile menu, cursor, scroll progress
 */
(function () {
  const isTouch = window.matchMedia('(pointer: coarse)').matches;

  const init = () => {
    const siteHeader = document.getElementById('siteHeader');
    const toTop = document.getElementById('toTop');

    const updateHeaderState = () => {
      siteHeader?.classList.toggle('scrolled', window.scrollY > 24);
      toTop?.classList.toggle('show', window.scrollY > 700);
    };
    window.addEventListener('scroll', updateHeaderState, { passive: true });
    updateHeaderState();

    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuClose = document.getElementById('mobileMenuClose');
    const mobileMenuBackdrop = document.getElementById('mobileMenuBackdrop');

    const closeMobileMenu = () => {
      mobileMenu?.classList.remove('open');
      document.body.classList.remove('menu-open');
      menuToggle?.setAttribute('aria-expanded', 'false');
      mobileMenu?.setAttribute('aria-hidden', 'true');
    };

    const openMobileMenu = () => {
      mobileMenu?.classList.add('open');
      document.body.classList.add('menu-open');
      menuToggle?.setAttribute('aria-expanded', 'true');
      mobileMenu?.setAttribute('aria-hidden', 'false');
    };

    menuToggle?.addEventListener('click', () => {
      if (mobileMenu?.classList.contains('open')) closeMobileMenu();
      else openMobileMenu();
    });
    mobileMenuClose?.addEventListener('click', closeMobileMenu);
    mobileMenuBackdrop?.addEventListener('click', closeMobileMenu);
    mobileMenu?.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeMobileMenu);
    });

    const progressBar = document.getElementById('scroll-progress');
    if (progressBar) {
      window.addEventListener('scroll', () => {
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        progressBar.style.width = height > 0 ? `${(window.scrollY / height) * 100}%` : '0%';
      }, { passive: true });
    }

    const sections = [...document.querySelectorAll('main section[id]')];
    const navLinks = [...document.querySelectorAll('.nav-link, .mobile-menu-nav a')];
    const setActiveNav = () => {
      const scrollPos = window.scrollY + 140;
      let currentId = sections[0]?.id || '';
      sections.forEach((section) => {
        if (scrollPos >= section.offsetTop) currentId = section.id;
      });
      navLinks.forEach((link) => {
        link.classList.toggle('active', link.getAttribute('href') === `#${currentId}`);
      });
    };
    setActiveNav();
    window.addEventListener('scroll', setActiveNav, { passive: true });

    const cursorDot = document.getElementById('cursor-dot');
    const cursorOutline = document.getElementById('cursor-outline');
    if (!isTouch && cursorDot && cursorOutline) {
      let mouseX = window.innerWidth / 2;
      let mouseY = window.innerHeight / 2;
      let outlineX = mouseX;
      let outlineY = mouseY;

      window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        cursorDot.style.transform = `translate(calc(${mouseX}px - 50%), calc(${mouseY}px - 50%))`;
      });

      const animateCursor = () => {
        outlineX += (mouseX - outlineX) * 0.15;
        outlineY += (mouseY - outlineY) * 0.15;
        cursorOutline.style.transform = `translate(calc(${outlineX}px - 50%), calc(${outlineY}px - 50%))`;
        requestAnimationFrame(animateCursor);
      };
      animateCursor();

      document.querySelectorAll('.interactable').forEach((el) => {
        el.addEventListener('mouseenter', () => cursorOutline.classList.add('hover-state'));
        el.addEventListener('mouseleave', () => cursorOutline.classList.remove('hover-state'));
      });
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
