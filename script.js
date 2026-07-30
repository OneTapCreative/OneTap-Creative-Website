(() => {
  'use strict';

  const FORM_TOKEN = '3770cd21b709b2fc75672c99acb98256';
  const FORM_ENDPOINT = `https://formsubmit.co/${FORM_TOKEN}`;
  const FORM_AJAX_ENDPOINT = `https://formsubmit.co/ajax/${FORM_TOKEN}`;
  const THANK_YOU_URL = 'https://onetapcreative.com/thank-you.html';
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
    form.action = FORM_ENDPOINT;
    ensureHidden('_captcha', 'false');
    ensureHidden('_next', THANK_YOU_URL);
    ensureHidden('_autoresponse', 'Thank you for contacting OneTap Creative. Your project request was received and will normally be reviewed within one business day. No payment was collected. If the project is a fit, the next steps are a written scope, client agreement, first payment, and the mobile onboarding portal.');

    const replyTo = ensureHidden('_replyto');
    const email = form.querySelector('input[name="Email"], input[type="email"]');
    const submitButton = form.querySelector('button[type="submit"]');
    const formNote = form.querySelector('.form-note');
    const originalButtonHtml = submitButton?.innerHTML || 'Request My Online Presence';
    const originalNote = formNote?.textContent || '';
    let submitting = false;

    const syncReplyTo = () => {
      if (replyTo && email) replyTo.value = email.value.trim();
    };

    const setSubmitting = (active, message = '') => {
      submitting = active;
      if (submitButton) {
        submitButton.disabled = active;
        submitButton.innerHTML = active
          ? 'Sending Request <span aria-hidden="true">…</span>'
          : originalButtonHtml;
      }
      if (formNote) formNote.textContent = message || originalNote;
    };

    email?.addEventListener('input', syncReplyTo);
    syncReplyTo();

    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (submitting || !form.reportValidity()) return;

      syncReplyTo();
      setSubmitting(true, 'Sending your request securely…');

      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: 'generate_lead', lead_type: 'website_project_request' });
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'generate_lead', { lead_type: 'website_project_request' });
      }

      try {
        const response = await fetch(FORM_AJAX_ENDPOINT, {
          method: 'POST',
          headers: { Accept: 'application/json' },
          body: new FormData(form)
        });
        const payload = await response.json().catch(() => ({}));

        if (!response.ok || payload.success === false) {
          throw new Error(payload.message || 'The form service did not accept the request.');
        }

        window.location.assign(THANK_YOU_URL);
      } catch (error) {
        console.error('OneTap form submission failed:', error);
        setSubmitting(false, 'The request could not be sent. Please check your connection and try again.');
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
