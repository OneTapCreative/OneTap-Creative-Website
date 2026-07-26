(() => {
  'use strict';

  const STORAGE_KEY = 'onetap-client-onboarding-v1';
  const MAX_UPLOAD_BYTES = 20 * 1024 * 1024;
  const SYSTEM_FIELDS = new Set(['_subject', '_template', '_captcha', '_next', '_honey', 'Plan', 'Portal Version', 'Onboarding Summary', 'Uploaded File Names']);

  const form = document.querySelector('#onboarding-form');
  const steps = [...document.querySelectorAll('.portal-step')];
  const progressLabel = document.querySelector('#progress-label');
  const progressPercent = document.querySelector('#progress-percent');
  const progressBar = document.querySelector('#progress-bar');
  const backButton = document.querySelector('#back-button');
  const nextButton = document.querySelector('#next-button');
  const submitButton = document.querySelector('#submit-button');
  const saveLaterButton = document.querySelector('#save-later');
  const saveStatus = document.querySelector('#save-status');
  const validationMessage = document.querySelector('#validation-message');
  const servicesList = document.querySelector('#services-list');
  const addServiceButton = document.querySelector('#add-service');
  const reviewSummary = document.querySelector('#review-summary');
  const summaryField = document.querySelector('#onboarding-summary');
  const fileListField = document.querySelector('#uploaded-file-list');
  const formNext = document.querySelector('#form-next');
  const imagePreview = document.querySelector('#image-preview');

  const stepNames = [
    'Welcome',
    'Business basics',
    'Website goal',
    'Services and pricing',
    'Brand and style',
    'Photos and content',
    'Contact setup',
    'Google Business Profile',
    'Review and submit'
  ];

  let currentStep = 0;
  let saveTimer = null;
  let submitting = false;
  let previewUrls = [];

  if (formNext) formNext.value = new URL('success.html', window.location.href).href;

  const escapeHtml = value => String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');

  const getNamedControls = name => [...form.elements].filter(element => element.name === name);

  const getFieldValue = name => {
    const controls = getNamedControls(name);
    if (!controls.length) return '';
    const first = controls[0];
    if (first.type === 'radio') return controls.find(control => control.checked)?.value || '';
    if (first.type === 'checkbox') return first.checked ? (first.value || 'Yes') : '';
    return first.value?.trim?.() ?? first.value ?? '';
  };

  const setFieldValue = (name, value) => {
    const controls = getNamedControls(name);
    if (!controls.length) return;
    const first = controls[0];
    if (first.type === 'radio') {
      controls.forEach(control => { control.checked = control.value === value; });
      return;
    }
    if (first.type === 'checkbox') {
      first.checked = value === true || value === first.value || value === 'Yes';
      return;
    }
    first.value = value ?? '';
  };

  const serviceRows = () => [...servicesList.querySelectorAll('.service-row')];

  const collectServices = () => serviceRows().map((row, index) => ({
    name: row.querySelector('[data-service-name]')?.value.trim() || '',
    description: row.querySelector('[data-service-description]')?.value.trim() || '',
    price: row.querySelector('[data-service-price]')?.value.trim() || '',
    public: row.querySelector('[data-service-public]')?.value || 'Use the overall pricing preference',
    order: index + 1
  }));

  const renumberServices = () => {
    serviceRows().forEach((row, index) => {
      const number = index + 1;
      row.querySelector('[data-service-title]').textContent = `Service ${number}`;
      row.querySelector('[data-service-name]').name = `Service ${number} Name`;
      row.querySelector('[data-service-description]').name = `Service ${number} Description`;
      row.querySelector('[data-service-price]').name = `Service ${number} Price`;
      row.querySelector('[data-service-public]').name = `Service ${number} Price Visibility`;
      row.querySelector('.remove-service').hidden = serviceRows().length === 1;
    });
  };

  const createServiceRow = (service = {}) => {
    const row = document.createElement('article');
    row.className = 'service-row';
    row.innerHTML = `
      <div class="service-row-header"><strong data-service-title>Service</strong><button class="remove-service" type="button">Remove</button></div>
      <label>Service name *<input data-service-name required placeholder="Example: Classic haircut" value="${escapeHtml(service.name || '')}" /></label>
      <label>Short description<textarea data-service-description rows="3" placeholder="What is included?">${escapeHtml(service.description || '')}</textarea></label>
      <div class="field-grid two-col">
        <label>Price or starting price<input data-service-price placeholder="Example: $45 or Starting at $300" value="${escapeHtml(service.price || '')}" /></label>
        <label>Show this price?<select data-service-public><option${service.public === 'Use the overall pricing preference' || !service.public ? ' selected' : ''}>Use the overall pricing preference</option><option${service.public === 'Yes' ? ' selected' : ''}>Yes</option><option${service.public === 'No' ? ' selected' : ''}>No</option></select></label>
      </div>`;
    row.querySelector('.remove-service').addEventListener('click', () => {
      if (serviceRows().length <= 1) return;
      row.remove();
      renumberServices();
      scheduleSave();
    });
    servicesList.appendChild(row);
    renumberServices();
  };

  const renderServices = services => {
    servicesList.innerHTML = '';
    const items = Array.isArray(services) && services.length ? services : [{ name: '', description: '', price: '' }];
    items.slice(0, 12).forEach(createServiceRow);
  };

  const collectDraft = () => {
    const fields = {};
    [...form.elements].forEach(element => {
      if (!element.name || SYSTEM_FIELDS.has(element.name) || element.type === 'file' || element.closest('.service-row')) return;
      if (element.type === 'radio') {
        if (element.checked) fields[element.name] = element.value;
      } else if (element.type === 'checkbox') {
        fields[element.name] = element.checked;
      } else {
        fields[element.name] = element.value;
      }
    });
    return {
      version: 1,
      currentStep,
      fields,
      services: collectServices(),
      savedAt: new Date().toISOString()
    };
  };

  const setSaveState = (text, saving = false) => {
    saveStatus.classList.toggle('is-saving', saving);
    const label = saveStatus.querySelector('span:last-child');
    if (label) label.textContent = text;
  };

  const saveDraft = () => {
    try {
      setSaveState('Saving…', true);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(collectDraft()));
      window.setTimeout(() => setSaveState('Progress saved on this device'), 250);
    } catch (error) {
      setSaveState('Unable to save in this browser');
    }
  };

  const scheduleSave = () => {
    setSaveState('Saving…', true);
    window.clearTimeout(saveTimer);
    saveTimer = window.setTimeout(saveDraft, 500);
  };

  const restoreDraft = () => {
    let draft = null;
    try {
      draft = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
    } catch (error) {
      draft = null;
    }

    renderServices(draft?.services);

    if (draft?.fields) {
      Object.entries(draft.fields).forEach(([name, value]) => setFieldValue(name, value));
      currentStep = Number.isInteger(draft.currentStep) ? Math.min(Math.max(draft.currentStep, 0), steps.length - 1) : 0;
      setSaveState('Saved progress restored');
    }

    const query = new URLSearchParams(window.location.search);
    const business = query.get('business');
    const email = query.get('email');
    if (business && !getFieldValue('Business Name')) setFieldValue('Business Name', business);
    if (email && !getFieldValue('Client Email')) setFieldValue('Client Email', email);
  };

  const setRequiredForPanel = (panel, required) => {
    panel.querySelectorAll('input,select,textarea').forEach(control => {
      if (control.dataset.neverRequired === 'true') return;
      control.required = required;
    });
  };

  const syncLocationFields = () => {
    const locationType = getFieldValue('Location Type');
    const addressPanel = document.querySelector('#address-fields');
    const serviceAreaPanel = document.querySelector('#service-area-fields');
    const showAddress = locationType === 'Public storefront or office';
    const showServiceArea = locationType === 'Service-area business';
    addressPanel.hidden = !showAddress;
    serviceAreaPanel.hidden = !showServiceArea;
    setRequiredForPanel(addressPanel, showAddress);
    setRequiredForPanel(serviceAreaPanel, showServiceArea);
  };

  const syncGoalFields = () => {
    const goal = getFieldValue('Primary Website Goal');
    const wrapper = document.querySelector('#goal-details');
    const booking = document.querySelector('#booking-fields');
    const quote = document.querySelector('#quote-fields');
    const phone = document.querySelector('#phone-fields');
    const showBooking = goal === 'Book an appointment';
    const showQuote = goal === 'Request a quote';
    const showPhone = goal === 'Call the business' || goal === 'Send a text';
    booking.hidden = !showBooking;
    quote.hidden = !showQuote;
    phone.hidden = !showPhone;
    wrapper.hidden = !(showBooking || showQuote || showPhone);
  };

  const syncGoogleFields = () => {
    const status = getFieldValue('Google Business Profile Status');
    document.querySelector('#gbp-existing').hidden = status !== 'Yes';
    document.querySelector('#gbp-new').hidden = status !== 'No';
  };

  const syncConditionals = () => {
    syncLocationFields();
    syncGoalFields();
    syncGoogleFields();
  };

  const clearValidation = () => {
    form.querySelectorAll('.is-invalid').forEach(element => element.classList.remove('is-invalid'));
    validationMessage.hidden = true;
  };

  const showValidation = message => {
    validationMessage.textContent = message;
    validationMessage.hidden = false;
    window.clearTimeout(showValidation.timer);
    showValidation.timer = window.setTimeout(() => { validationMessage.hidden = true; }, 6000);
  };

  const isVisible = element => !element.closest('[hidden]') && element.type !== 'hidden';

  const validateStep = stepIndex => {
    clearValidation();
    const step = steps[stepIndex];
    const requiredControls = [...step.querySelectorAll('[required]')].filter(isVisible);
    const invalid = [];
    const processedRadioNames = new Set();

    requiredControls.forEach(control => {
      if (control.type === 'radio') {
        if (processedRadioNames.has(control.name)) return;
        processedRadioNames.add(control.name);
        const group = [...step.querySelectorAll(`input[type="radio"][name="${CSS.escape(control.name)}"]`)];
        if (!group.some(item => item.checked)) invalid.push(group[0]);
        return;
      }
      if (control.type === 'checkbox' && !control.checked) {
        invalid.push(control);
        return;
      }
      if (!control.checkValidity() || !String(control.value || '').trim()) invalid.push(control);
    });

    if (stepIndex === 3) {
      const namedServices = collectServices().filter(service => service.name);
      if (!namedServices.length) invalid.push(servicesList.querySelector('[data-service-name]'));
    }

    if (invalid.length) {
      invalid.forEach(control => control?.classList.add('is-invalid'));
      const target = invalid[0];
      target?.focus({ preventScroll: true });
      target?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      showValidation('Please complete the highlighted required information before continuing.');
      return false;
    }
    return true;
  };

  const prefillContactFields = () => {
    const inquiryEmail = getNamedControls('Inquiry Email')[0];
    const inquiryPhone = getNamedControls('Inquiry Phone')[0];
    if (inquiryEmail && !inquiryEmail.value) inquiryEmail.value = getFieldValue('Client Email');
    if (inquiryPhone && !inquiryPhone.value) inquiryPhone.value = getFieldValue('Business Phone');
  };

  const formatAddress = () => {
    if (getFieldValue('Location Type') === 'Service-area business') return getFieldValue('Service Area');
    return [getFieldValue('Street Address'), getFieldValue('Address City'), getFieldValue('Address State'), getFieldValue('ZIP Code')].filter(Boolean).join(', ');
  };

  const fileInputs = () => [...form.querySelectorAll('input[type="file"]')];
  const selectedFiles = () => fileInputs().flatMap(input => [...(input.files || [])]);
  const totalUploadBytes = () => selectedFiles().reduce((total, file) => total + file.size, 0);

  const updateFileDisplays = () => {
    previewUrls.forEach(url => URL.revokeObjectURL(url));
    previewUrls = [];
    imagePreview.innerHTML = '';

    fileInputs().forEach(input => {
      const status = input.closest('.upload-card')?.querySelector('.file-status');
      const files = [...(input.files || [])];
      if (status) status.textContent = files.length ? `${files.length} file${files.length === 1 ? '' : 's'} selected` : (input.multiple ? 'No files selected' : 'No file selected');
      files.filter(file => file.type.startsWith('image/')).slice(0, 10).forEach(file => {
        const url = URL.createObjectURL(file);
        previewUrls.push(url);
        const image = document.createElement('img');
        image.src = url;
        image.alt = `Preview of ${file.name}`;
        imagePreview.appendChild(image);
      });
    });

    if (totalUploadBytes() > MAX_UPLOAD_BYTES) showValidation('Your selected files are over 20 MB. Please remove or compress some files before submitting.');
  };

  const reviewValue = (label, value) => value ? `<dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd>` : '';

  const buildReview = () => {
    const services = collectServices().filter(service => service.name);
    const files = selectedFiles();
    const cards = [
      {
        step: 1,
        title: 'Business information',
        rows: [
          ['Business', getFieldValue('Business Name')], ['Contact', getFieldValue('Primary Contact')],
          ['Email', getFieldValue('Client Email')], ['Phone', getFieldValue('Business Phone')],
          ['Business type', getFieldValue('Business Type')], ['Location', formatAddress()],
          ['Hours', getFieldValue('Business Hours')], ['Description', getFieldValue('Business Description')]
        ]
      },
      {
        step: 2,
        title: 'Website goal',
        rows: [
          ['Primary action', getFieldValue('Primary Website Goal')], ['Success goal', getFieldValue('Website Success Goal')],
          ['Booking link', getFieldValue('Booking Link')], ['Booking instructions', getFieldValue('Booking Instructions')],
          ['Quote questions', getFieldValue('Quote Request Questions')], ['Public contact number', getFieldValue('Public Contact Number')]
        ]
      },
      {
        step: 3,
        title: 'Services and pricing',
        rows: [
          ['Services', services.map(service => `${service.name}${service.price ? ` — ${service.price}` : ''}`).join('; ')],
          ['Pricing display', getFieldValue('Pricing Display')], ['Payment methods', getFieldValue('Payment Methods')]
        ]
      },
      {
        step: 4,
        title: 'Brand direction',
        rows: [
          ['Style', getFieldValue('Website Style')], ['Preferred colors', getFieldValue('Preferred Colors')],
          ['Colors to avoid', getFieldValue('Colors to Avoid')], ['Brand personality', getFieldValue('Brand Personality')],
          ['Social links', getFieldValue('Social Media Links')]
        ]
      },
      {
        step: 5,
        title: 'Photos and content',
        rows: [
          ['Selected files', files.length ? files.map(file => file.name).join(', ') : 'No files selected'],
          ['Image help', getFieldValue('Image Help')], ['Required content', getFieldValue('Required Website Content')]
        ]
      },
      {
        step: 6,
        title: 'Customer contact',
        rows: [
          ['Inquiry email', getFieldValue('Inquiry Email')], ['Inquiry phone', getFieldValue('Inquiry Phone')],
          ['Response time', getFieldValue('Response Time')], ['Instructions', getFieldValue('Customer Contact Instructions')]
        ]
      },
      {
        step: 7,
        title: 'Google Business Profile',
        rows: [
          ['Current status', getFieldValue('Google Business Profile Status')],
          ['Existing profile', getFieldValue('Existing Google Profile Link')],
          ['Official name', getFieldValue('Official Google Business Name')],
          ['Category', getFieldValue('Preferred Google Category')],
          ['Opening date', getFieldValue('Business Opening Date')]
        ]
      },
      {
        step: 0,
        title: 'Plan and website management',
        rows: [
          ['Plan', '$179/month · 3-month minimum · $537 initial commitment'],
          ['Website', 'One mobile-first page with up to approximately 8–10 sections'],
          ['Revisions', 'Two organized prelaunch revision rounds'],
          ['Monthly updates', 'Up to 30 minutes; unused time does not roll over'],
          ['Domain', 'Provided and connected by OneTap Creative while the plan is active']
        ]
      }
    ];

    reviewSummary.innerHTML = cards.map(card => `
      <article class="review-card">
        <div class="review-card-head"><h3>${escapeHtml(card.title)}</h3><button type="button" data-edit-step="${card.step}">Edit</button></div>
        <dl>${card.rows.map(([label, value]) => reviewValue(label, value)).join('')}</dl>
      </article>`).join('');

    reviewSummary.querySelectorAll('[data-edit-step]').forEach(button => button.addEventListener('click', () => {
      currentStep = Number(button.dataset.editStep);
      showStep();
    }));

    const plainSummary = cards.map(card => `${card.title}: ${card.rows.filter(([, value]) => value).map(([label, value]) => `${label}=${value}`).join(' | ')}`).join('\n');
    summaryField.value = plainSummary;
    fileListField.value = files.map(file => file.name).join(', ');
  };

  const showStep = () => {
    steps.forEach((step, index) => {
      const active = index === currentStep;
      step.classList.toggle('is-active', active);
      step.setAttribute('aria-hidden', active ? 'false' : 'true');
    });

    if (currentStep === 6) prefillContactFields();
    if (currentStep === 8) buildReview();

    const percent = currentStep === 0 ? 0 : Math.round((currentStep / (steps.length - 1)) * 100);
    progressLabel.textContent = stepNames[currentStep];
    progressPercent.textContent = `${percent}%`;
    progressBar.style.width = `${percent}%`;
    backButton.hidden = currentStep === 0;
    nextButton.hidden = currentStep === steps.length - 1;
    submitButton.hidden = currentStep !== steps.length - 1;
    nextButton.textContent = currentStep === 0 ? 'Start onboarding' : currentStep === 7 ? 'Review answers' : 'Continue';
    clearValidation();
    syncConditionals();
    saveDraft();
    window.scrollTo({ top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  };

  nextButton.addEventListener('click', () => {
    if (!validateStep(currentStep)) return;
    currentStep = Math.min(currentStep + 1, steps.length - 1);
    showStep();
  });

  backButton.addEventListener('click', () => {
    currentStep = Math.max(currentStep - 1, 0);
    showStep();
  });

  addServiceButton.addEventListener('click', () => {
    if (serviceRows().length >= 12) {
      showValidation('The standard portal supports up to 12 services. Additional services can be discussed with OneTap.');
      return;
    }
    createServiceRow();
    serviceRows().at(-1)?.querySelector('[data-service-name]')?.focus();
    scheduleSave();
  });

  saveLaterButton.addEventListener('click', () => {
    saveDraft();
    setSaveState('Saved. You can close this page and return on this device.');
    saveLaterButton.textContent = 'Saved ✓';
    window.setTimeout(() => { saveLaterButton.textContent = 'Save & finish later'; }, 2500);
  });

  form.addEventListener('input', event => {
    event.target.classList.remove('is-invalid');
    scheduleSave();
  });

  form.addEventListener('change', event => {
    event.target.classList.remove('is-invalid');
    syncConditionals();
    if (event.target.type === 'file') updateFileDisplays();
    scheduleSave();
  });

  form.addEventListener('submit', event => {
    if (!validateStep(8)) {
      event.preventDefault();
      return;
    }
    if (totalUploadBytes() > MAX_UPLOAD_BYTES) {
      event.preventDefault();
      showValidation('Your selected files are over 20 MB. Please remove or compress some files before submitting.');
      return;
    }
    buildReview();
    submitting = true;
    submitButton.disabled = true;
    submitButton.textContent = 'Submitting…';
    setSaveState('Submitting onboarding…', true);
  });

  window.addEventListener('beforeunload', event => {
    if (!submitting && selectedFiles().length) {
      event.preventDefault();
      event.returnValue = '';
    }
  });

  restoreDraft();
  syncConditionals();
  updateFileDisplays();
  showStep();
})();
