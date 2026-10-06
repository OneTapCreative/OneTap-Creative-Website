(() => {
  'use strict';

  const FORM_RECIPIENT = 'hello@onetapcreative.com';
  const FORM_ACTION = `https://formsubmit.co/${FORM_RECIPIENT}`;
  const SUCCESS_URL = new URL('/onboarding/success', window.location.origin).href;
  const form = document.querySelector('#onboarding-form');

  if (form) {
    form.action = FORM_ACTION;

    const ensureHidden = (name, value = '') => {
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

    ensureHidden('_next', SUCCESS_URL);
    ensureHidden('_autoresponse', 'Thanks — we received your OneTap Creative onboarding. We’ll review your business details, content, and uploads to make sure we have everything needed to begin. If anything is missing, we’ll contact you from hello@onetapcreative.com. Once your onboarding is complete, the first website review is typically ready within 7–10 business days.');

    const replyTo = ensureHidden('_replyto');
    const email = form.querySelector('#client-email');
    const syncReplyTo = () => { if (replyTo && email) replyTo.value = email.value.trim(); };
    email?.addEventListener('input', syncReplyTo);
    form.addEventListener('submit', syncReplyTo);
    syncReplyTo();

    const params = new URLSearchParams(window.location.search);
    const requestedPlan = (params.get('plan') || '').toLowerCase();
    const planMap = {
      start: 'OneTap Start — $99/month',
      grow: 'OneTap Grow — $149/month'
    };
    const selectedPlan = planMap[requestedPlan];
    if (selectedPlan) {
      const radio = [...form.querySelectorAll('input[name="Selected Plan"]')].find(input => input.value === selectedPlan);
      if (radio) radio.checked = true;
      ensureHidden('Payment Redirect Plan', selectedPlan);
    }
  }

  const core = document.createElement('script');
  core.src = '/onboarding/onboarding-core.js?v=hard-launch-2';
  core.defer = true;
  document.body.appendChild(core);
})();