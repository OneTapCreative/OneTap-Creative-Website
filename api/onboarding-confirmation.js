const ALLOWED_PLANS = new Set([
  'OneTap Start — $99/month',
  'OneTap Grow — $149/month'
]);

const PROD_ORIGINS = new Set([
  'https://onetapcreative.com',
  'https://www.onetapcreative.com'
]);

const escapeHtml = (value = '') => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#039;');

const clean = (value, max = 160) => String(value || '').trim().slice(0, max);

const isEmail = value => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

const originAllowed = req => {
  const origin = String(req.headers.origin || '');
  const referer = String(req.headers.referer || '');
  if (!origin && !referer) return false;
  if (PROD_ORIGINS.has(origin)) return true;
  if (origin.endsWith('.vercel.app')) return true;
  if ([...PROD_ORIGINS].some(item => referer.startsWith(item))) return true;
  return /https:\/\/[^/]+\.vercel\.app\//.test(referer);
};

const planLabel = plan => {
  if (plan === 'OneTap Grow — $149/month') return 'OneTap Grow';
  return 'OneTap Start';
};

const buildText = ({ name, business, plan }) => {
  const greeting = name ? `Hi ${name},` : 'Hi there,';
  const businessLine = business ? ` for ${business}` : '';
  return `${greeting}

You’re all set.

Thanks for completing your OneTap Creative onboarding${businessLine}. We received everything you submitted for ${planLabel(plan)}.

What happens next:
1. We review your onboarding details, content, and uploads.
2. If anything is missing, we’ll contact you from hello@onetapcreative.com.
3. Once everything required is complete, your first website review is typically ready within 7–10 business days.

Need to add something? Reply to this email and we’ll help.

OneTap Creative
https://onetapcreative.com
hello@onetapcreative.com`;
};

const buildHtml = ({ name, business, plan }) => {
  const safeName = escapeHtml(name);
  const safeBusiness = escapeHtml(business);
  const safePlan = escapeHtml(planLabel(plan));
  const greeting = safeName ? `Hi ${safeName},` : 'Hi there,';
  const businessLine = safeBusiness ? ` for <strong style="color:#f5f2e8;">${safeBusiness}</strong>` : '';

  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="color-scheme" content="dark">
  <meta name="supported-color-schemes" content="dark">
  <title>Onboarding received | OneTap Creative</title>
</head>
<body style="margin:0;padding:0;background:#080808;color:#f5f2e8;font-family:Arial,Helvetica,sans-serif;">
  <div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;">
    Your OneTap Creative onboarding is in. Here’s what happens next.
  </div>
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;background:#080808;">
    <tr>
      <td align="center" style="padding:32px 16px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;max-width:620px;">
          <tr>
            <td style="padding:0 0 18px 0;">
              <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="border-collapse:collapse"><tr><td style="vertical-align:middle;padding-right:10px"><img src="https://onetapcreative.com/assets/images/onetap-icon-natural.png" alt="" width="48" height="48" style="display:block;width:48px;height:48px;border:0"></td><td style="vertical-align:middle"><div style="font-family:Arial,Helvetica,sans-serif;font-size:26px;font-weight:800;letter-spacing:-1px;line-height:1"><span style="color:#ffffff">One</span><span style="color:#d6ad3c">Tap</span></div><div style="font-family:Arial,Helvetica,sans-serif;font-size:10px;font-weight:700;letter-spacing:4px;color:#f5f2e8;padding-top:5px">CREATIVE</div></td></tr></table>
            </td>
          </tr>
          <tr>
            <td style="border:1px solid #27251f;border-radius:22px;background:#11110f;padding:34px 34px 30px 34px;">
              <div style="font-size:12px;line-height:1.3;letter-spacing:.18em;text-transform:uppercase;color:#f0cf6a;font-weight:700;margin-bottom:14px;">
                Onboarding received
              </div>
              <h1 style="margin:0 0 14px 0;font-size:40px;line-height:1.04;letter-spacing:-.035em;color:#f5f2e8;font-weight:800;">
                You’re all set.
              </h1>
              <p style="margin:0 0 12px 0;font-size:17px;line-height:1.65;color:#d8d4c9;">${greeting}</p>
              <p style="margin:0 0 24px 0;font-size:17px;line-height:1.65;color:#d8d4c9;">
                Thanks for completing your OneTap Creative onboarding${businessLine}. We received everything you submitted for <strong style="color:#f5f2e8;">${safePlan}</strong>.
              </p>

              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;margin:0 0 26px 0;background:#171713;border:1px solid #2d2b24;border-radius:16px;">
                <tr>
                  <td style="padding:18px 20px;">
                    <div style="font-size:12px;line-height:1.3;letter-spacing:.12em;text-transform:uppercase;color:#9d998f;font-weight:700;margin-bottom:5px;">Status</div>
                    <div style="font-size:17px;line-height:1.45;color:#f5f2e8;font-weight:700;">Received and ready for review</div>
                  </td>
                </tr>
              </table>

              <h2 style="margin:0 0 14px 0;font-size:21px;line-height:1.25;color:#f5f2e8;">What happens next</h2>

              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;">
                <tr>
                  <td valign="top" width="38" style="padding:0 0 18px 0;">
                    <div style="width:28px;height:28px;border-radius:999px;background:#f0cf6a;color:#080808;font-size:13px;font-weight:800;text-align:center;line-height:28px;">1</div>
                  </td>
                  <td valign="top" style="padding:1px 0 18px 0;">
                    <div style="font-size:16px;line-height:1.4;color:#f5f2e8;font-weight:700;">We review your onboarding</div>
                    <div style="font-size:14px;line-height:1.6;color:#aaa69d;margin-top:3px;">We check your business details, content, photos, and uploads.</div>
                  </td>
                </tr>
                <tr>
                  <td valign="top" width="38" style="padding:0 0 18px 0;">
                    <div style="width:28px;height:28px;border-radius:999px;background:#24221d;color:#f0cf6a;font-size:13px;font-weight:800;text-align:center;line-height:28px;border:1px solid #3b382f;">2</div>
                  </td>
                  <td valign="top" style="padding:1px 0 18px 0;">
                    <div style="font-size:16px;line-height:1.4;color:#f5f2e8;font-weight:700;">We contact you only if something is missing</div>
                    <div style="font-size:14px;line-height:1.6;color:#aaa69d;margin-top:3px;">Any follow-up will come from hello@onetapcreative.com.</div>
                  </td>
                </tr>
                <tr>
                  <td valign="top" width="38" style="padding:0;">
                    <div style="width:28px;height:28px;border-radius:999px;background:#24221d;color:#f0cf6a;font-size:13px;font-weight:800;text-align:center;line-height:28px;border:1px solid #3b382f;">3</div>
                  </td>
                  <td valign="top" style="padding:1px 0 0 0;">
                    <div style="font-size:16px;line-height:1.4;color:#f5f2e8;font-weight:700;">Your first website review</div>
                    <div style="font-size:14px;line-height:1.6;color:#aaa69d;margin-top:3px;">Once all required content is complete, the target is typically 7–10 business days.</div>
                  </td>
                </tr>
              </table>

              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;margin-top:28px;">
                <tr>
                  <td>
                    <a href="https://onetapcreative.com/" style="display:inline-block;background:#f0cf6a;color:#080808;text-decoration:none;font-size:14px;line-height:1;font-weight:800;padding:15px 20px;border-radius:999px;">Visit OneTap Creative</a>
                  </td>
                </tr>
              </table>

              <div style="height:1px;background:#2a2822;margin:30px 0 22px 0;"></div>

              <p style="margin:0;font-size:14px;line-height:1.65;color:#aaa69d;">
                Need to add something or ask a question? Just reply to this email.<br>
                <a href="mailto:hello@onetapcreative.com" style="color:#f0cf6a;text-decoration:none;">hello@onetapcreative.com</a>
              </p>
            </td>
          </tr>
          <tr>
            <td style="padding:18px 6px 0 6px;font-size:12px;line-height:1.6;color:#77736b;">
              OneTap Creative · Professional websites for local service businesses<br>
              <a href="https://onetapcreative.com/" style="color:#9d998f;text-decoration:none;">onetapcreative.com</a>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`;
};

const parseBody = req => {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string') {
    try { return JSON.parse(req.body); } catch (error) { return {}; }
  }
  return {};
};

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'GET') {
    if (req.query?.preview === '1') {
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      return res.status(200).send(buildHtml({
        name: 'Jordan',
        business: 'Golden Valley Home Services',
        plan: 'OneTap Grow — $149/month'
      }));
    }

    return res.status(200).json({
      ready: process.env.ONETAP_BRANDED_EMAIL_ENABLED === 'true'
        && Boolean(process.env.RESEND_API_KEY && process.env.ONETAP_EMAIL_FROM)
    });
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ ok: false, error: 'method_not_allowed' });
  }

  if (!originAllowed(req)) {
    return res.status(403).json({ ok: false, error: 'origin_not_allowed' });
  }

  const payload = parseBody(req);
  if (payload.website) return res.status(204).end();

  const email = clean(payload.email, 254).toLowerCase();
  const name = clean(payload.name, 100);
  const business = clean(payload.business, 140);
  const plan = clean(payload.plan, 80);
  const submissionId = clean(payload.submissionId, 120);

  if (!isEmail(email) || !ALLOWED_PLANS.has(plan) || !submissionId) {
    return res.status(400).json({ ok: false, error: 'invalid_payload' });
  }

  const enabled = process.env.ONETAP_BRANDED_EMAIL_ENABLED === 'true';
  const apiKey = process.env.RESEND_API_KEY;
  const from = clean(process.env.ONETAP_EMAIL_FROM, 180);
  const replyTo = clean(process.env.ONETAP_EMAIL_REPLY_TO || 'hello@onetapcreative.com', 180);

  if (!enabled || !apiKey || !from) {
    return res.status(503).json({ ok: false, error: 'email_not_configured' });
  }

  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'Idempotency-Key': `onetap-onboarding/${submissionId}`.slice(0, 256)
    },
    body: JSON.stringify({
      from,
      to: [email],
      reply_to: replyTo,
      subject: 'You’re all set — OneTap Creative onboarding received',
      html: buildHtml({ name, business, plan }),
      text: buildText({ name, business, plan })
    })
  });

  const result = await response.json().catch(() => ({}));

  if (!response.ok) {
    console.error('Resend onboarding confirmation failed', {
      status: response.status,
      error: result?.message || result?.name || 'unknown'
    });
    return res.status(502).json({ ok: false, error: 'email_send_failed' });
  }

  return res.status(200).json({ ok: true, id: result.id || null });
}
