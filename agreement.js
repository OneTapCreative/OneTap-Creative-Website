(() => {
  const form = document.getElementById('agreement-form');
  const DIRECT_FORMSUBMIT_DESTINATION = atob('Y2xhcmVuY2Uud29ya2Zsb3dAZ21haWwuY29t');
  const plan = document.getElementById('agreement-plan');
  const planName = document.getElementById('agreement-plan-name');
  const planPrice = document.getElementById('agreement-plan-price');
  const planTotal = document.getElementById('agreement-plan-total');
  const name = document.getElementById('agreement-name');
  const business = document.getElementById('agreement-business');
  const email = document.getElementById('agreement-email');
  const signature = document.getElementById('agreement-signature');
  const replyTo = document.getElementById('agreement-replyto');
  const emailCopy = document.getElementById('agreement-client-email-copy');
  const timestamp = document.getElementById('agreement-timestamp');
  const pageUrl = document.getElementById('agreement-page-url');
  const next = document.getElementById('agreement-next');

  document.querySelectorAll('#year').forEach(el => el.textContent = new Date().getFullYear());
  if (!form || !plan) return;

  // Force fresh FormSubmit activation for the current private agreement origin.
  form.action = `https://formsubmit.co/${DIRECT_FORMSUBMIT_DESTINATION}`;

  const plans = {
    start: { value:'OneTap Start — $99/month', name:'OneTap Start', price:'$99/month', detail:'3-month minimum · $297 initial total', total:'$297' },
    grow: { value:'OneTap Grow — $149/month', name:'OneTap Grow', price:'$149/month', detail:'3-month minimum · $447 initial total', total:'$447' }
  };

  const setSummary = () => {
    const chosen = Object.values(plans).find(p => p.value === plan.value);
    if (!chosen) {
      planName.textContent = 'Choose a plan below';
      planPrice.textContent = 'Monthly price will appear here.';
      planTotal.value = '';
      return;
    }
    planName.textContent = chosen.name;
    planPrice.textContent = chosen.price + ' · ' + chosen.detail;
    planTotal.value = chosen.total;
  };

  const params = new URLSearchParams(window.location.search);
  const requestedPlan = (params.get('plan') || '').toLowerCase();
  if (plans[requestedPlan]) plan.value = plans[requestedPlan].value;
  if (params.get('name')) name.value = params.get('name');
  if (params.get('business')) business.value = params.get('business');
  if (params.get('email')) email.value = params.get('email');

  setSummary();
  plan.addEventListener('change', setSummary);
  const syncEmail = () => {
    const value = email.value.trim();
    replyTo.value = value;
    if (emailCopy) emailCopy.value = value;
  };
  email.addEventListener('input', syncEmail);
  syncEmail();

  form.addEventListener('submit', (event) => {
    const normalizedName = name.value.trim().replace(/\s+/g, ' ').toLowerCase();
    const normalizedSignature = signature.value.trim().replace(/\s+/g, ' ').toLowerCase();
    if (!normalizedName || normalizedSignature !== normalizedName) {
      event.preventDefault();
      signature.setCustomValidity('Please type the same full legal name shown above.');
      signature.reportValidity();
      signature.focus();
      return;
    }
    signature.setCustomValidity('');
    syncEmail();
    timestamp.value = new Date().toISOString();
    pageUrl.value = window.location.href;
    next.value = 'https://one-tap-creative-website-git-main-clarenceworkflows-projects.vercel.app/agreement-received.html';
  });

  signature.addEventListener('input', () => signature.setCustomValidity(''));
})();