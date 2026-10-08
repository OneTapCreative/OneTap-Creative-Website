const ORIGINS = new Set(['https://onetapcreative.com', 'https://www.onetapcreative.com']);
const clean = (value, max = 120) => String(value || '').trim().slice(0, max);
const escapeHtml = value => clean(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
const validEmail = value => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
const allowedOrigin = req => {
  const origin = String(req.headers.origin || '');
  const referer = String(req.headers.referer || '');
  return ORIGINS.has(origin) || [...ORIGINS].some(item => referer.startsWith(item + '/'));
};
const ready = () => process.env.ONETAP_BRANDED_EMAIL_ENABLED === 'true' &&
  Boolean(process.env.RESEND_API_KEY && process.env.ONETAP_EMAIL_FROM);

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'GET') return res.status(200).json({ ready: ready() });
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'method_not_allowed' });
  if (!allowedOrigin(req)) return res.status(403).json({ ok: false, error: 'origin_not_allowed' });
  if (!ready()) return res.status(503).json({ ok: false, error: 'email_not_configured' });
  const data = typeof req.body === 'object' && req.body ? req.body : {};
  if (data.website) return res.status(204).end();
  const email = clean(data.email, 254).toLowerCase();
  const name = clean(data.name, 100);
  const business = clean(data.business, 140);
  const submissionId = clean(data.submissionId, 120);
  if (!validEmail(email) || !submissionId) return res.status(400).json({ ok: false, error: 'invalid_payload' });

  const greeting = name ? `Hi ${name},` : 'Hi there,';
  const safeGreeting = name ? `Hi ${escapeHtml(name)},` : 'Hi there,';
  const businessText = business ? ` for ${business}` : '';
  const businessHtml = business ? ` for <strong style="color:#f5f2e8">${escapeHtml(business)}</strong>` : '';
  const text = `${greeting}

Thanks for reaching out to OneTap Creative${businessText}. We received your website request.

Here's what happens next:
1. We review your business and goals.
2. We'll personally follow up within one business day with questions or a recommended next step.
3. If we're a good fit, we'll confirm the scope and plan before any payment.

No payment has been collected. Have a question? Reply to this email.

OneTap Creative
hello@onetapcreative.com
https://onetapcreative.com`;
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0;background:#080808;color:#f5f2e8;font-family:Arial,Helvetica,sans-serif"><div style="display:none;max-height:0;overflow:hidden">We received your website request. Here's what happens next.</div><table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#080808"><tr><td align="center" style="padding:28px 16px"><table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:620px"><tr><td style="padding-bottom:20px"><img src="https://onetapcreative.com/assets/images/onetap-logo-full-natural.png" width="164" alt="OneTap Creative" style="display:block;border:0;max-width:100%;height:auto"></td></tr><tr><td style="background:#11110f;border:1px solid #302a1d;border-radius:20px;padding:32px"><p style="margin:0 0 12px;color:#f0cf6a;text-transform:uppercase;letter-spacing:.16em;font-size:12px;font-weight:700">Request received</p><h1 style="color:#f5f2e8;font-size:36px;margin:0 0 20px">Thanks for reaching out.</h1><p style="color:#d8d4c9;font-size:16px;line-height:1.65">${safeGreeting}</p><p style="color:#d8d4c9;font-size:16px;line-height:1.65">We received your website request${businessHtml}. Thanks for considering OneTap Creative.</p><h2 style="color:#f5f2e8;font-size:21px;margin:26px 0 12px">What happens next</h2><p style="color:#d8d4c9;line-height:1.75;font-size:15px"><strong style="color:#f0cf6a">01.</strong> We review your business and goals.<br><strong style="color:#f0cf6a">02.</strong> We'll personally follow up within one business day.<br><strong style="color:#f0cf6a">03.</strong> If we're a fit, we'll confirm the plan and scope before payment.</p><p style="background:#1b1913;border-radius:12px;padding:15px;color:#d8d4c9;font-size:14px;line-height:1.6">No payment has been collected.</p><p style="margin-top:26px;color:#aaa69d;font-size:14px;line-height:1.6">Have a question? Just reply to this email.<br><a style="color:#f0cf6a" href="mailto:hello@onetapcreative.com">hello@onetapcreative.com</a></p></td></tr><tr><td style="padding:18px 4px;color:#77736b;font-size:12px">OneTap Creative · <a style="color:#aaa69d" href="https://onetapcreative.com/">onetapcreative.com</a></td></tr></table></td></tr></table></body></html>`;
  let response;
  try {
    response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json', 'Idempotency-Key': `onetap-lead/${submissionId}` },
      body: JSON.stringify({
        from: process.env.ONETAP_EMAIL_FROM, to: [email],
        reply_to: process.env.ONETAP_EMAIL_REPLY_TO || 'hello@onetapcreative.com',
        subject: 'We received your request — OneTap Creative', html, text
      })
    });
  } catch (error) {
    console.error('Resend lead confirmation request failed', error?.message || 'network_error');
    return res.status(502).json({ ok: false, error: 'email_request_failed' });
  }
  const result = await response.json().catch(() => ({}));
  if (!response.ok) {
    console.error('Resend lead confirmation failed', { status: response.status, error: result?.message || 'unknown' });
    return res.status(502).json({ ok: false, error: 'email_send_failed' });
  }
  return res.status(200).json({ ok: true, id: result.id || null });
}
