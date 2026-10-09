(() => {
  'use strict';

  const FORM_RECIPIENT = 'hello@onetapcreative.com';
  const FORM_ACTION = `https://formsubmit.co/${FORM_RECIPIENT}`;
  const FORM_AJAX_ACTION = `https://formsubmit.co/ajax/${FORM_RECIPIENT}`;
  const SUCCESS_URL = new URL('/thank-you', window.location.origin).href;
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
    ensureHidden('_autoresponse', 'Thanks for reaching out to OneTap Creative. We received your project request and will review it within one business day. If we need anything else, we’ll contact you from hello@onetapcreative.com. If the project is a fit, we’ll confirm the plan and next steps before any payment is collected.');

    // Check branded email readiness before submitting to FormSubmit so it
    // cannot also send a second plain-text customer autoresponse.
    let brandReady = false;
    const readyController = new AbortController();
    const readyTimeout = window.setTimeout(() => readyController.abort(), 5000);
    const readiness = fetch('/api/lead-confirmation', {
      headers: { Accept: 'application/json' }, cache: 'no-store', signal: readyController.signal
    }).then(response => response.ok ? response.json() : null)
      .then(data => { brandReady = Boolean(data?.ready); })
      .catch(() => { brandReady = false; })
      .finally(() => window.clearTimeout(readyTimeout));

    const autoresponse = form.querySelector('input[name="_autoresponse"]');
    const newSubmissionId = () => window.crypto?.randomUUID?.() ||
      `${Date.now()}-${Math.random().toString(36).slice(2)}`;
    const confirmationPayload = () => ({
      submissionId: newSubmissionId(),
      email: email?.value.trim() || '',
      name: form.querySelector('input[name="Full Name"]')?.value.trim() || '',
      business: form.querySelector('input[name="Business Name"]')?.value.trim() || ''
    });

    const replyTo = ensureHidden('_replyto');
    const email = form.querySelector('input[name="Email"], input[type="email"]');
    const submitButton = form.querySelector('button[type="submit"]');
    const status = createStatus();
    const originalButtonHtml = submitButton?.innerHTML || 'Submit';
    const syncReplyTo = () => { if (replyTo && email) replyTo.value = email.value.trim(); };

    const phone = form.querySelector('input[name="Phone"]');
    const checkPhone = () => {
      if (!phone) return;
      const value = phone.value.trim();
      const digits = value.replace(/\D/g, '');
      const validCharacters = /^[+\d\s().-]+$/.test(value);
      const validLength = digits.length === 10 || (digits.length === 11 && digits.startsWith('1'));
      phone.setCustomValidity(!value || (validCharacters && validLength) ? '' : 'Enter a valid 10-digit phone number (or 11 digits starting with 1).');
    };
    phone?.addEventListener('input', checkPhone);
    phone?.addEventListener('blur', checkPhone);
    email?.addEventListener('input', syncReplyTo);
    syncReplyTo();

    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (form.dataset.submitting === 'true') return;
      checkPhone();
      if (!form.reportValidity()) return;

      syncReplyTo();
      await readiness;
      const useBranded = brandReady;
      if (useBranded) autoresponse?.remove();
      const leadConfirmation = useBranded ? confirmationPayload() : null;
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

        if (leadConfirmation) {
          try {
            const confirmationResponse = await fetch('/api/lead-confirmation', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
              body: JSON.stringify(leadConfirmation)
            });
            if (!confirmationResponse.ok) console.warn('Branded lead confirmation could not be sent. Check Vercel logs.');
          } catch (error) {
            console.warn('Branded lead confirmation request failed.', error);
          }
        }
        if (status) status.textContent = 'Request received. Opening your confirmation…';
        window.setTimeout(() => window.location.assign(SUCCESS_URL), 450);
      } catch (error) {
        console.warn('AJAX submission unavailable; using secure form fallback.', error);
        if (status) status.textContent = 'Opening the secure submission confirmation…';
        form.action = FORM_ACTION;
        // Fall back to FormSubmit customer response if its AJAX request fails.
        if (!form.querySelector('input[name="_autoresponse"]')) {
          ensureHidden('_autoresponse', 'Thanks for reaching out to OneTap Creative. We received your website request and will follow up within one business day.');
        }
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


  const planInterest = document.querySelector('#plan-interest');
  const serviceHidden = document.querySelector('#website-service-hidden');
  document.querySelectorAll('[data-plan]').forEach(link => {
    link.addEventListener('click', () => {
      if (!planInterest) return;
      const plan = link.dataset.plan || '';
      const option = Array.from(planInterest.options).find(item => item.value.startsWith(plan + ' —'));
      if (option) {
        planInterest.value = option.value;
        if (serviceHidden) serviceHidden.value = option.value;
      }
    });
  });
  planInterest?.addEventListener('change', () => {
    if (serviceHidden) serviceHidden.value = planInterest.value || 'Plan to be confirmed after fit review';
  });

  document.querySelectorAll('.demo-trust span').forEach(item => {
    if (item.textContent.includes('5.0 reviews')) item.textContent = 'Trust section';
  });
  const stars = document.querySelector('.profile-body .stars');
  if (stars?.textContent.includes('5.0')) stars.textContent = 'Business profile preview';
  const profileType = document.querySelector('.profile-body .stars + p');
  if (profileType) profileType.textContent = 'Example layout';

  const core = document.createElement('script');
  core.src = '/script-core.js?v=final-qa-1';
  core.defer = true;
  document.body.appendChild(core);
})();