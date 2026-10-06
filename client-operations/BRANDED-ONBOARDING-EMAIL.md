# OneTap Creative Branded Onboarding Email

This workflow adds a branded transactional confirmation email after a client successfully submits the onboarding portal.

## Architecture

Client onboarding form → FormSubmit internal delivery → onboarding success page → OneTap Vercel API → Resend → branded client confirmation.

FormSubmit remains the internal onboarding record. Resend handles only the polished client-facing confirmation.

## Brand treatment

The email matches OneTap Creative:

- dark charcoal background
- warm gold accent
- OneTap logo
- concise “You’re all set” heading
- onboarding status card
- three clear next steps
- 7–10 business-day first-review target
- reply-to: hello@onetapcreative.com
- responsive single-column email layout

Preview:

`https://onetapcreative.com/api/onboarding-confirmation?preview=1`

## Required Vercel environment variables

Set these in the OneTap Vercel project:

- `RESEND_API_KEY` — secret Resend API key
- `ONETAP_EMAIL_FROM` — recommended: `OneTap Creative <hello@onetapcreative.com>` after Resend verifies the sending domain
- `ONETAP_EMAIL_REPLY_TO` — `hello@onetapcreative.com`
- `ONETAP_BRANDED_EMAIL_ENABLED` — keep `false` until verification/testing is complete; then set to `true`

Use Production environment. Preview can be added later if desired.

## Safe fallback behavior

Until `ONETAP_BRANDED_EMAIL_ENABLED=true` and the required Resend settings exist, the onboarding form keeps the existing FormSubmit plain autoresponse.

When the branded system is ready, the browser detects it and removes the FormSubmit autoresponse before submission so the client receives only one confirmation email.

## Resend domain setup

1. Create/connect the Resend account.
2. Add `onetapcreative.com` as the sending domain.
3. Add only the DNS records Resend specifically provides.
4. Do not remove or overwrite working Google Workspace MX, SPF, DKIM, or DMARC records.
5. Wait for Resend to show the domain as verified.
6. Create an API key with sending permission.
7. Add the Vercel environment variables above.
8. Redeploy the production site.
9. Confirm `/api/onboarding-confirmation` returns `{"ready":true}`.
10. Submit a real onboarding test with a separate email.

## Acceptance test

The migration is complete when:

- internal onboarding submission still arrives at hello@onetapcreative.com
- onboarding success page loads
- client receives one branded OneTap confirmation email
- From name is OneTap Creative
- Reply goes to hello@onetapcreative.com
- email renders cleanly on mobile and desktop Gmail
- duplicate refreshes do not create duplicate sends
- FormSubmit plain autoresponse is not also delivered when branded email is active

## Security

The server endpoint:

- uses a fixed OneTap email template
- accepts only Start/Grow plan values
- accepts only same-site / Vercel-origin requests
- does not expose the Resend API key to the browser
- uses Resend idempotency keys to reduce duplicate sends
- does not accept custom subjects or arbitrary email content
