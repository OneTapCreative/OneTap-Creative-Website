const header = document.querySelector('.site-header');
const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.main-nav');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

window.addEventListener('scroll', () => header?.classList.toggle('scrolled', window.scrollY > 12), { passive: true });

const setNavigationState = (isOpen, { returnFocus = false } = {}) => {
  if (!nav || !navToggle) return;

  nav.classList.toggle('open', isOpen);
  document.body.classList.toggle('nav-open', isOpen);
  navToggle.setAttribute('aria-expanded', String(isOpen));
  navToggle.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');

  if (returnFocus && !isOpen) navToggle.focus({ preventScroll: true });
};

navToggle?.addEventListener('click', event => {
  event.stopPropagation();
  setNavigationState(navToggle.getAttribute('aria-expanded') !== 'true');
});

// Close the menu when the user taps away, presses Escape, or rotates/resizes the phone.
document.addEventListener('click', event => {
  if (!nav?.classList.contains('open')) return;
  if (nav.contains(event.target) || navToggle?.contains(event.target)) return;
  setNavigationState(false);
});

document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && nav?.classList.contains('open')) {
    setNavigationState(false, { returnFocus: true });
  }
});

window.addEventListener('resize', () => {
  if (window.innerWidth >= 960 && nav?.classList.contains('open')) setNavigationState(false);
}, { passive: true });

// Pause the animated mini-sites while the page itself is moving. This leaves more
// rendering capacity for smooth mobile anchor scrolling.
let scrollIdleTimer = 0;
window.addEventListener('scroll', () => {
  document.documentElement.classList.add('is-page-scrolling');
  window.clearTimeout(scrollIdleTimer);
  scrollIdleTimer = window.setTimeout(() => {
    document.documentElement.classList.remove('is-page-scrolling');
  }, 140);
}, { passive: true });

// One delegated anchor handler keeps the order reliable on mobile:
// 1) hide the dropdown immediately, 2) measure the target, 3) start native smooth scroll.
document.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#"]');
  if (!link) return;

  const href = link.getAttribute('href');
  if (!href || href === '#' || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

  const target = href === '#top' ? document.documentElement : document.querySelector(href);
  if (!target) return;

  event.preventDefault();
  const menuWasOpen = Boolean(nav?.classList.contains('open'));
  setNavigationState(false);

  const scrollToTarget = () => {
    const headerOffset = (header?.getBoundingClientRect().height || 0) + 10;
    const targetY = href === '#top'
      ? 0
      : Math.max(0, target.getBoundingClientRect().top + window.scrollY - headerOffset);

    window.scrollTo({
      top: targetY,
      left: 0,
      behavior: prefersReducedMotion ? 'auto' : 'smooth'
    });

    if (window.location.hash !== href) history.pushState(null, '', href);
  };

  // Two paint frames ensure the fixed dropdown is gone before scrolling begins.
  if (menuWasOpen) {
    requestAnimationFrame(() => requestAnimationFrame(scrollToTarget));
  } else {
    scrollToTarget();
  }
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
