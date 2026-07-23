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

const selectedDisplay = document.querySelector('#selected-plan-display strong');
const selectedInput = document.querySelector('#selected-plan-input');
const planButtons = [...document.querySelectorAll('.price-row')];
planButtons.forEach(button => {
  button.addEventListener('click', () => {
    const plan = button.dataset.plan;
    planButtons.forEach(item => {
      const selected = item === button;
      item.classList.toggle('selected', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    if (selectedDisplay) selectedDisplay.textContent = plan;
    if (selectedInput) selectedInput.value = plan;
    document.querySelector('#start')?.scrollIntoView({ behavior: 'smooth' });
  });
});

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
