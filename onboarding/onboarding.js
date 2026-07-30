(() => {
  'use strict';

  const FORM_ID = '3770cd21b709b2fc75672c99acb98256';
  const FORM_ACTION = `https://formsubmit.co/${FORM_ID}`;
  const SUCCESS_URL = 'https://onetapcreative.com/onboarding/success.html';
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

    ensureHidden('_captcha', 'false');
    ensureHidden('_next', SUCCESS_URL);
    ensureHidden('_autoresponse', 'OneTap Creative received your completed onboarding form. Your business information and uploaded files will be reviewed. You will be contacted if anything is missing before production begins.');

    const replyTo = ensureHidden('_replyto');
    const email = form.querySelector('#client-email');
    const syncReplyTo = () => { if (replyTo && email) replyTo.value = email.value.trim(); };
    email?.addEventListener('input', syncReplyTo);
    form.addEventListener('submit', syncReplyTo);
    syncReplyTo();
  }

  const core = document.createElement('script');
  core.src = 'onboarding-core.js?v=hard-launch-1';
  core.defer = true;
  document.body.appendChild(core);
})();