const header = document.querySelector('.site-header');
const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.main-nav');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

window.addEventListener('scroll', () => header?.classList.toggle('scrolled', window.scrollY > 12), { passive: true });

navToggle?.addEventListener('click', () => {
  const open = navToggle.getAttribute('aria-expanded') === 'true';
  navToggle.setAttribute('aria-expanded', String(!open));
  navToggle.setAttribute('aria-label', open ? 'Open navigation' : 'Close navigation');
  nav?.classList.toggle('open', !open);
});

document.querySelectorAll('.main-nav a').forEach(link => link.addEventListener('click', () => {
  nav?.classList.remove('open');
  navToggle?.setAttribute('aria-expanded', 'false');
  navToggle?.setAttribute('aria-label', 'Open navigation');
}));

// Smooth, header-aware anchor movement with a natural ease-in/ease-out curve.
let activeScrollFrame = 0;
const cancelActiveScroll = () => {
  if (activeScrollFrame) cancelAnimationFrame(activeScrollFrame);
  activeScrollFrame = 0;
};
['wheel', 'touchstart'].forEach(type => window.addEventListener(type, cancelActiveScroll, { passive: true }));

document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', event => {
    const href = link.getAttribute('href');
    if (!href || href === '#' || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const target = href === '#top' ? document.documentElement : document.querySelector(href);
    if (!target) return;
    event.preventDefault();
    cancelActiveScroll();

    const headerOffset = (header?.offsetHeight || 0) + 10;
    const startY = window.scrollY;
    const targetY = href === '#top' ? 0 : Math.max(0, target.getBoundingClientRect().top + startY - headerOffset);
    const distance = targetY - startY;

    if (prefersReducedMotion || Math.abs(distance) < 2) {
      window.scrollTo(0, targetY);
      history.pushState(null, '', href);
      return;
    }

    const duration = Math.min(950, Math.max(520, Math.abs(distance) * 0.32));
    const startedAt = performance.now();
    const easeInOutCubic = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

    const step = now => {
      const progress = Math.min(1, (now - startedAt) / duration);
      window.scrollTo(0, startY + distance * easeInOutCubic(progress));
      if (progress < 1) {
        activeScrollFrame = requestAnimationFrame(step);
      } else {
        activeScrollFrame = 0;
        history.pushState(null, '', href);
      }
    };
    activeScrollFrame = requestAnimationFrame(step);
  });
});


const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

document.querySelectorAll('details').forEach(detail => {
  detail.addEventListener('toggle', () => {
    if (!detail.open) return;
    document.querySelectorAll('details[open]').forEach(other => {
      if (other !== detail) other.open = false;
    });
  });
});

const mobileCta = document.querySelector('.mobile-cta');
const heroPrimary = document.querySelector('.hero .btn');
if (mobileCta && heroPrimary && 'IntersectionObserver' in window) {
  const mobileCtaObserver = new IntersectionObserver(([entry]) => {
    mobileCta.classList.toggle('visible', !entry.isIntersecting);
  }, { threshold: 0.25 });
  mobileCtaObserver.observe(heroPrimary);
}

const reduceMotion = prefersReducedMotion;
const videos = [...document.querySelectorAll('video')];
if (reduceMotion) {
  videos.forEach(video => video.pause());
} else if ('IntersectionObserver' in window) {
  const videoObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const video = entry.target;
      if (entry.isIntersecting) {
        video.play().catch(() => {});
      } else {
        video.pause();
      }
    });
  }, { rootMargin: '180px 0px', threshold: 0.05 });
  videos.forEach(video => {
    video.setAttribute('disablepictureinpicture', '');
    videoObserver.observe(video);
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      videos.forEach(video => video.pause());
    } else {
      videos.filter(video => video.getBoundingClientRect().bottom > -180 && video.getBoundingClientRect().top < window.innerHeight + 180)
        .forEach(video => video.play().catch(() => {}));
    }
  });
}

const year = document.querySelector('#year');
if (year) year.textContent = new Date().getFullYear();


// Build absolute launch URLs at runtime so the site works on Vercel previews and the final custom domain.
const canonicalLink = document.querySelector('#canonical-link');
const ogUrl = document.querySelector('#og-url');
const ogImage = document.querySelector('#og-image');
const formNextUrl = document.querySelector('#form-next-url');
const businessSchema = document.querySelector('#business-schema');
const homeUrl = new URL('index.html', window.location.href).href.replace(/index\.html$/, '');
if (canonicalLink) canonicalLink.href = homeUrl;
if (ogUrl) ogUrl.content = homeUrl;
if (ogImage) ogImage.content = new URL('assets/images/onetap-og-natural.jpg', window.location.href).href;
if (formNextUrl) formNextUrl.value = new URL('thank-you.html', window.location.href).href;
if (businessSchema) {
  try {
    const schema = JSON.parse(businessSchema.textContent);
    schema.url = homeUrl;
    schema.image = new URL('assets/images/onetap-og-natural.jpg', window.location.href).href;
    businessSchema.textContent = JSON.stringify(schema);
  } catch (_) {}
}

// Lightweight conversion events. These become useful automatically if a dataLayer is added later.
document.querySelectorAll('a[href="#start"]').forEach(link => link.addEventListener('click', () => {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event: 'onetap_cta_click', cta_text: link.textContent.trim() });
}));
document.querySelector('#lead-form')?.addEventListener('submit', () => {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event: 'onetap_lead_submit' });
});
