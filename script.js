(() => {
  'use strict';

  const FORM_EMAIL = 'clarence.workflow@gmail.com';
  const form = document.querySelector('#lead-form');

  const ensureHidden = (name, value = '') => {
    if (!form) return null;
    let field = form.querySelector(`input[name="${name}"]`);
    if (!field) {
      field = document.createElement('input');
      field.type = 'hidden';
      field.name = name;
      form.appendChild(field);
    }
    field.value = value;
    return field;
  };

  if (form) {
    form.action = `https://formsubmit.co/${FORM_EMAIL}`;
    ensureHidden('_autoresponse', 'Thank you for contacting OneTap Creative. Your project request was received and will normally be reviewed within one business day. No payment was collected. If the project is a fit, the next steps are a written scope, client agreement, first payment, and the mobile onboarding portal.');
    const replyTo = ensureHidden('_replyto');
    const email = form.querySelector('input[name="Email"], input[type="email"]');
    const syncReplyTo = () => { if (replyTo && email) replyTo.value = email.value.trim(); };
    email?.addEventListener('input', syncReplyTo);
    syncReplyTo();

    form.addEventListener('submit', () => {
      syncReplyTo();
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: 'generate_lead', lead_type: 'website_project_request' });
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'generate_lead', { lead_type: 'website_project_request' });
      }
    });
  }

  document.querySelectorAll('.demo-trust span').forEach(item => {
    if (item.textContent.includes('5.0 reviews')) item.textContent = 'Trust section';
  });
  const stars = document.querySelector('.profile-body .stars');
  if (stars?.textContent.includes('5.0')) stars.textContent = 'Business profile preview';
  const profileType = document.querySelector('.profile-body .stars + p');
  if (profileType) profileType.textContent = 'Example layout';

  const core = document.createElement('script');
  core.src = 'script-core.js?v=hard-launch-1';
  core.defer = true;
  document.body.appendChild(core);
})();
