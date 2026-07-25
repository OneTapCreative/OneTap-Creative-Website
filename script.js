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

// Keep the public offer aligned with OneTap Creative's approved agency standard.
// The plan includes a comprehensive launch foundation, not an unlimited monthly SEO campaign.
const seoCopyReplacements = [
  ['Basic local SEO', 'Advanced SEO foundation'],
  ['basic local SEO', 'advanced SEO foundation'],
  ['Basic SEO and Google-ready launch', 'Advanced SEO foundation and Google-ready launch']
];

const replaceSeoText = root => {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const textNodes = [];
  while (walker.nextNode()) textNodes.push(walker.currentNode);

  textNodes.forEach(node => {
    let updatedText = node.nodeValue;
    seoCopyReplacements.forEach(([from, to]) => {
      updatedText = updatedText.replaceAll(from, to);
    });
    if (updatedText !== node.nodeValue) node.nodeValue = updatedText;
  });
};

replaceSeoText(document.body);

document.title = 'OneTap Creative | Websites, Advanced SEO & Google Visibility';

const metaDescription = document.querySelector('meta[name="description"]');
if (metaDescription) {
  metaDescription.content = 'OneTap Creative helps local businesses get found online with a mobile-friendly website, advanced SEO foundation, Google Business Profile setup, domain, hosting, updates, and support for $149 per month.';
}

const ogDescription = document.querySelector('meta[property="og:description"]');
if (ogDescription) {
  ogDescription.content = 'A complete online presence for local businesses: professional website, advanced SEO foundation, Google Business Profile setup, domain, hosting, and ongoing support.';
}

const advancedSeoCard = [...document.querySelectorAll('.presence-feature')]
  .find(card => card.querySelector('h3')?.textContent.trim() === 'Advanced SEO foundation');
if (advancedSeoCard) {
  const description = advancedSeoCard.querySelector('p');
  if (description) {
    description.textContent = 'Keyword-focused structure, technical SEO, metadata, schema, mobile performance, sitemap and indexing setup, Search Console, and local search signals.';
  }
}

const visibilitySteps = document.querySelectorAll('.visibility-checklist > div');
if (visibilitySteps[1]) {
  const title = visibilitySteps[1].querySelector('strong');
  const text = visibilitySteps[1].querySelector('span');
  if (title) title.textContent = 'Advanced on-page and technical foundation';
  if (text) {
    text.innerHTML = '<strong>Advanced on-page and technical foundation</strong>Keyword mapping, search-friendly structure, metadata, schema, performance, sitemap, and indexing setup.';
  }
}
if (visibilitySteps[2]) {
  const text = visibilitySteps[2].querySelector('span');
  if (text) {
    text.innerHTML = '<strong>Search Console and visibility monitoring</strong>Ownership setup, sitemap submission, indexing review, and basic ongoing health checks after launch.';
  }
}

const faqList = document.querySelector('.faq-list');
if (faqList && !document.querySelector('#advanced-seo-faq')) {
  const seoFaq = document.createElement('details');
  seoFaq.id = 'advanced-seo-faq';
  seoFaq.className = 'reveal visible';
  seoFaq.innerHTML = '<summary>What does the advanced SEO foundation include?<span>+</span></summary><p>Every standard launch includes local keyword mapping, search-focused headings and page structure, title and description optimization, technical SEO, mobile and performance optimization, image optimization, canonical setup, structured data when appropriate, sitemap and indexing setup, Google Search Console, and local business information alignment. Ongoing blog writing, backlink campaigns, paid advertising, ecommerce SEO, multi-location campaigns, and guaranteed rankings are not included in the standard $149 plan and may require a separate proposal.</p>';
  faqList.prepend(seoFaq);
  seoFaq.addEventListener('toggle', () => {
    if (!seoFaq.open) return;
    document.querySelectorAll('details[open]').forEach(other => {
      if (other !== seoFaq) other.open = false;
    });
  });
}

// Build absolute launch URLs at runtime so the site works on Vercel previews and the final custom domain.
const canonicalLink = document.querySelector('#canonical-link');
const ogUrl = document.querySelector('#og-url');
const ogImage = document.querySelector('#og-image');
const formNextUrl = document.querySelector('#form-next-url');
const businessSchema = document.querySelector('#business-schema');
const homeUrl = new URL('index.html', window.location.href).href.replace(/index\.html$/, '');
if (canonicalLink) canonicalLink.href = homeUrl;
if (ogUrl) ogUrl.content = homeUrl;
if (ogImage) ogImage.content = new URL('assets/images/onetap-og-direction.jpg', window.location.href).href;
if (formNextUrl) formNextUrl.value = new URL('thank-you.html', window.location.href).href;
if (businessSchema) {
  try {
    const schema = JSON.parse(businessSchema.textContent);
    schema.url = homeUrl;
    schema.image = new URL('assets/images/onetap-og-direction.jpg', window.location.href).href;
    schema.description = 'Complete online presence service for local businesses including mobile-first website design, domain and hosting, Google Business Profile setup, an advanced SEO foundation, Google indexing, Search Console setup, updates, and ongoing support.';
    schema.knowsAbout = [
      'Mobile-first web design',
      'Local business websites',
      'Google Business Profile setup',
      'Advanced on-page SEO',
      'Technical SEO foundations',
      'Local SEO',
      'Google Search Console',
      'Booking websites',
      'Quote request websites'
    ];
    schema.hasOfferCatalog = {
      '@type': 'OfferCatalog',
      name: 'Complete Online Presence Plan',
      itemListElement: [{
        '@type': 'Offer',
        price: '149',
        priceCurrency: 'USD',
        category: 'Website design and SEO services',
        itemOffered: {
          '@type': 'Service',
          name: 'Complete Online Presence Plan',
          description: 'Mobile-friendly website, domain and hosting, Google Business Profile setup or optimization, advanced SEO foundation, Search Console setup, updates, maintenance, and support.'
        }
      }]
    };
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
