const header = document.querySelector('.site-header');
const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.main-nav');

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

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
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
  videos.forEach(video => videoObserver.observe(video));
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
if (ogImage) ogImage.content = new URL('assets/images/onetap-og.png', window.location.href).href;
if (formNextUrl) formNextUrl.value = new URL('thank-you.html', window.location.href).href;
if (businessSchema) {
  try {
    const schema = JSON.parse(businessSchema.textContent);
    schema.url = homeUrl;
    schema.image = new URL('assets/images/onetap-og.png', window.location.href).href;
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
