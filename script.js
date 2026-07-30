(() => {
  'use strict';

  const FORM_ID = '3770cd21b709b2fc75672c99acb98256';
  const FORM_ACTION = `https://formsubmit.co/${FORM_ID}`;
  const FORM_AJAX_ACTION = `https://formsubmit.co/ajax/${FORM_ID}`;
  const SUCCESS_URL = 'https://onetapcreative.com/thank-you.html';
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

  const createStatus = () => {
    if (!form) return null;
    let status = form.querySelector('#lead-form-status');
    if (status) return status;
    status = document.createElement('p');
    status.id = 'lead-form-status';
    status.className = 'form-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.style.minHeight = '1.5em';
    status.style.margin = '12px 0 0';
    const note = form.querySelector('.form-note');
    if (note) form.insertBefore(status, note);
    else form.appendChild(status);
    return status;
  };

  const isSuccessfulResponse = payload => {
    if (!payload || typeof payload !== 'object') return false;
    if (payload.success === true || payload.success === 'true') return true;
    return typeof payload.message === 'string' && /success|submitted|received/i.test(payload.message);
  };

  if (form) {
    form.action = FORM_ACTION;
    ensureHidden('_captcha', 'false');
    ensureHidden('_next', SUCCESS_URL);
    ensureHidden('_autoresponse', 'Thank you for contacting OneTap Creative. Your project request was received and will normally be reviewed within one business day. No payment was collected. If the project is a fit, the next steps are a written scope, client agreement, first payment, and the mobile onboarding portal.');

    const replyTo = ensureHidden('_replyto');
    const email = form.querySelector('input[name="Email"], input[type="email"]');
    const submitButton = form.querySelector('button[type="submit"]');
    const status = createStatus();
    const originalButtonHtml = submitButton?.innerHTML || 'Submit';
    const syncReplyTo = () => { if (replyTo && email) replyTo.value = email.value.trim(); };

    email?.addEventListener('input', syncReplyTo);
    syncReplyTo();

    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (form.dataset.submitting === 'true') return;
      if (!form.reportValidity()) return;

      syncReplyTo();
      form.dataset.submitting = 'true';
      form.setAttribute('aria-busy', 'true');
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = 'Sending…';
      }
      if (status) status.textContent = 'Sending your request securely…';

      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: 'generate_lead', lead_type: 'website_project_request' });
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'generate_lead', { lead_type: 'website_project_request' });
      }

      try {
        const response = await fetch(FORM_AJAX_ACTION, {
          method: 'POST',
          headers: { Accept: 'application/json' },
          body: new FormData(form)
        });
        const payload = await response.json().catch(() => ({}));
        if (!response.ok || !isSuccessfulResponse(payload)) {
          throw new Error(payload.message || `Submission failed with status ${response.status}`);
        }

        if (status) status.textContent = 'Request received. Opening your confirmation…';
        window.setTimeout(() => window.location.assign(SUCCESS_URL), 450);
      } catch (error) {
        console.warn('AJAX submission unavailable; using secure form fallback.', error);
        if (status) status.textContent = 'Opening the secure submission confirmation…';
        form.action = FORM_ACTION;
        ensureHidden('_next', SUCCESS_URL);
        window.setTimeout(() => HTMLFormElement.prototype.submit.call(form), 150);
      } finally {
        window.setTimeout(() => {
          if (document.visibilityState === 'visible' && window.location.href !== SUCCESS_URL) {
            form.dataset.submitting = 'false';
            form.removeAttribute('aria-busy');
            if (submitButton) {
              submitButton.disabled = false;
              submitButton.innerHTML = originalButtonHtml;
            }
          }
        }, 8000);
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