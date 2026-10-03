(function () {
  'use strict';

  function toggleFaq(item) {
    const isOpen = item.classList.contains('active');
    document.querySelectorAll('#faq .faq-item').forEach((other) => {
      other.classList.remove('active');
    });
    if (!isOpen) {
      item.classList.add('active');
    }
  }

  function initFaq() {
    const wrap = document.querySelector('#faq .faq-wrap');
    if (!wrap || wrap.dataset.faqBound) return;
    wrap.dataset.faqBound = '1';

    wrap.addEventListener('click', (event) => {
      const btn = event.target.closest('.faq-q');
      if (!btn) return;
      event.preventDefault();
      const item = btn.closest('.faq-item');
      if (item) toggleFaq(item);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFaq);
  } else {
    initFaq();
  }
})();
