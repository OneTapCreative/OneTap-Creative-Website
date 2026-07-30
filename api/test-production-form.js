module.exports = async function handler(req, res) {
  const expectedToken = 'onetap-form-qa-20260730-8e4d7c1a';

  if (req.method !== 'GET' || req.query.token !== expectedToken) {
    res.status(404).json({ ok: false });
    return;
  }

  const testId = `ONETAP-FORM-QA-${new Date().toISOString().replace(/[-:.]/g, '')}`;
  const fields = new URLSearchParams({
    _subject: `TEST - OneTap Creative Website Form QA - ${testId}`,
    _template: 'table',
    _captcha: 'false',
    _replyto: 'codicta12@gmail.com',
    _autoresponse: 'This is an automated OneTap Creative website form test. No response is required.',
    _next: 'https://onetapcreative.com/thank-you.html',
    'Website Service': '$179/month Complete Online Presence Plan — TEST SUBMISSION',
    'Full Name': 'OneTap Form Test',
    'Business Name': 'OneTap QA Test Business',
    Email: 'codicta12@gmail.com',
    Phone: '209-555-0199',
    'Business Type': 'Other service that needs bookings or quotes',
    'Primary Website Goal': 'Submit a contact form',
    'Google Business Profile Status': 'Not sure',
    'Website Goals': `TEST ONLY: Verify delivery, formatting, and redirect. Test ID ${testId}`,
    'Current Website or Social': 'https://onetapcreative.com/',
    'Preferred Launch Timing': 'Not sure yet',
    'Lead Source': 'Website QA test',
    'Service Terms Accepted': 'Yes',
    'UTM Source': 'internal-qa',
    'UTM Medium': 'form-test',
    'UTM Campaign': 'hard-launch-qa',
    'Landing Page': 'https://onetapcreative.com/'
  });

  try {
    const response = await fetch('https://formsubmit.co/clarence.workflow@gmail.com', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'OneTapCreative-Production-Form-QA/1.0'
      },
      body: fields.toString(),
      redirect: 'follow'
    });

    const body = await response.text();
    res.status(200).json({
      ok: response.ok,
      testId,
      formServiceStatus: response.status,
      finalUrl: response.url,
      responsePreview: body.replace(/\s+/g, ' ').slice(0, 700)
    });
  } catch (error) {
    res.status(500).json({
      ok: false,
      testId,
      error: error instanceof Error ? error.message : String(error)
    });
  }
};
