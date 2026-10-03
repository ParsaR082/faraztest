/**
 * Video section player
 */
(function initVideoSection() {
  const toEmbedUrl = (url) => {
    if (!url) return '';
    const ytMatch = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)/);
    if (ytMatch) return `https://www.youtube.com/embed/${ytMatch[1]}?autoplay=1&rel=0`;
    const aparatMatch = url.match(/aparat\.com\/v\/([\w]+)/);
    if (aparatMatch) return `https://www.aparat.com/video/video/embed/videohash/${aparatMatch[1]}/autoplay/true`;
    return url;
  };

  const playerWrap = document.getElementById('videoPlayerWrap');
  if (!playerWrap) return;

  const renderPlayer = (poster, title, cap, videoUrl) => {
    playerWrap.innerHTML = '';
    const player = document.createElement('div');
    player.className = 'video-player';
    player.id = 'mainVideoPlayer';

    if (videoUrl) {
      const iframe = document.createElement('iframe');
      iframe.src = toEmbedUrl(videoUrl);
      iframe.allow = 'autoplay; fullscreen';
      iframe.allowFullscreen = true;
      player.appendChild(iframe);
    } else {
      const img = document.createElement('img');
      img.className = 'video-poster';
      img.src = poster;
      img.alt = title;
      img.loading = 'lazy';
      player.appendChild(img);

      const btn = document.createElement('button');
      btn.className = 'video-play-btn interactable';
      btn.setAttribute('aria-label', 'پخش ویدیو');
      btn.innerHTML = '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
      player.appendChild(btn);
    }

    const info = document.createElement('div');
    info.className = 'video-player-info';
    info.innerHTML = `<h3>${title}</h3>${cap ? `<p>${cap}</p>` : ''}`;
    if (!videoUrl) player.appendChild(info);

    playerWrap.appendChild(player);
    return player;
  };

  const playVideo = (thumb) => {
    const url = thumb.dataset.video;
    const poster = thumb.dataset.poster;
    const title = thumb.dataset.title || '';
    const cap = thumb.dataset.caption || '';

    document.querySelectorAll('.video-thumb').forEach((t) => t.classList.remove('active'));
    thumb.classList.add('active');
    renderPlayer(poster, title, cap, url || null);
  };

  document.querySelectorAll('.video-thumb').forEach((thumb) => {
    thumb.addEventListener('click', () => playVideo(thumb));
  });

  const mainPlayer = document.getElementById('mainVideoPlayer');
  mainPlayer?.querySelector('.video-play-btn')?.addEventListener('click', () => {
    const url = mainPlayer.dataset?.video;
    if (url) {
      renderPlayer(
        mainPlayer.querySelector('.video-poster')?.src || '',
        mainPlayer.dataset.title || '',
        mainPlayer.dataset.caption || '',
        url
      );
    }
  });
})();
