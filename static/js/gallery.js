/**
 * Gallery lightbox
 */
(function initGalleryLightbox() {
  const lightbox = document.getElementById('galleryLightbox');
  const content = document.getElementById('lightboxContent');
  const caption = document.getElementById('lightboxCaption');
  const closeBtn = document.getElementById('lightboxClose');
  if (!lightbox || !content) return;

  const toEmbedUrl = (url) => {
    if (!url) return '';
    const ytMatch = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)/);
    if (ytMatch) return `https://www.youtube.com/embed/${ytMatch[1]}?autoplay=1`;
    const aparatMatch = url.match(/aparat\.com\/v\/([\w]+)/);
    if (aparatMatch) return `https://www.aparat.com/video/video/embed/videohash/${aparatMatch[1]}/autoplay/true`;
    return url;
  };

  const closeLightbox = () => {
    lightbox.classList.remove('active');
    lightbox.setAttribute('aria-hidden', 'true');
    content.innerHTML = '';
    caption.innerHTML = '';
    document.body.style.overflow = '';
  };

  const openLightbox = (item) => {
    const type = item.dataset.type;
    const title = item.dataset.title || '';
    const cap = item.dataset.caption || '';
    content.innerHTML = '';

    if (type === 'video' && item.dataset.video) {
      const iframe = document.createElement('iframe');
      iframe.src = toEmbedUrl(item.dataset.video);
      iframe.allow = 'autoplay; fullscreen';
      iframe.allowFullscreen = true;
      content.appendChild(iframe);
    } else {
      const src = item.dataset.src || item.querySelector('img')?.src;
      if (src) {
        const img = document.createElement('img');
        img.src = src;
        img.alt = title;
        content.appendChild(img);
      }
    }

    caption.innerHTML = title ? `<h3>${title}</h3>${cap ? `<p>${cap}</p>` : ''}` : '';
    lightbox.classList.add('active');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };

  document.querySelectorAll('.gallery-item').forEach((item) => {
    item.addEventListener('click', () => openLightbox(item));
  });

  closeBtn?.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
  });
})();
