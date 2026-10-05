# External Account Activation

These actions require the business owner's account access, identity verification, DNS control, payment authorization, or legal approval. Complete them with `launch/OWNER-CHECKLIST.md`.

## Professional email

Permanent domain purchased: `onetapcreative.com`. Planned professional mailbox: `hello@onetapcreative.com`.

Until then, keep the existing verified secure FormSubmit delivery route in place. After the permanent domain is connected:

1. Create and verify the professional mailbox.
2. Configure the email provider's current SPF, DKIM, and DMARC DNS records.
3. Test sending to Gmail and Outlook/Hotmail.
4. Reply from both test accounts and confirm delivery is not going to spam.
5. Migrate **both** secure FormSubmit routes together and reactivate/test the new route before retiring the current verified delivery route.

Do not expose a personal inbox in public HTML, JavaScript, or client-facing documentation.

## Square Contracts — client agreement

Follow `client-operations/SQUARE-CONTRACT-SOP.md`.

Create two reusable Square Contract templates:
- **OneTap Start — Client Service Agreement**
- **OneTap Grow — Client Service Agreement**

Use Square's Service Agreement template as the base. Send the matching contract after discovery and plan confirmation. Wait until Square shows the agreement as signed/completed before sending any payment link. Keep the completed PDF in Square and attach it to the related transaction/project when useful.

## Square recurring payment — credit/debit card only at launch

Follow `client-operations/SQUARE-CARD-PAYMENT-SOP.md`.

Create two recurring products:
- **OneTap Start — $99 monthly**
- **OneTap Grow — $149 monthly**

The signed Square Contract—not the payment link by itself—defines the three-month minimum and selected scope.

- Accept credit/debit card for the current launch workflow.
- Disable tipping.
- Do not enable ACH/bank transfer, Afterpay, Cash App Pay, or gift cards for the recurring OneTap launch workflow.
- Collect client name, business name, email, and selected plan where supported.
- Test recurring checkout, automatic monthly billing, correct onboarding redirect, and receipt behavior for both Start and Grow.
- Confirm failed-payment, card-update, cancellation, plan-change, and refund handling.
- Keep the public homepage inquiry-only; send the correct payment link only after fit, plan recommendation, scope, and agreement approval.
- Send the personalized onboarding URL only after payment is confirmed.

## Analytics

The website already records UTM values, CTA clicks, portfolio clicks, lead submission events, and `generate_lead` hooks.

- Enable Vercel Web Analytics for baseline traffic measurement.
- Create GA4 if detailed marketing attribution/conversion reporting is needed.
- Add the production GA4 Measurement ID only after the real property exists.
- Verify page views and a test `generate_lead` event in production before paid advertising.

## Search Console

Long-term Search Console activation is deferred until the permanent custom domain is purchased. The temporary public URL is:

`https://onetapcreative.com/`

The canonical/schema/sitemap/social URLs now use the permanent domain. Next: verify the **Domain property** in Google Search Console using DNS, submit the permanent sitemap, inspect the homepage, and record the starting search baseline.

## Google Business Profile

Create a OneTap Creative Google Business Profile only if the business currently meets Google's eligibility requirements. Use truthful public business information and complete required verification through the owner's account. Do not create an ineligible or misleading profile simply for SEO.

Client Business Profiles remain **client-owned**. OneTap should receive Manager access rather than taking primary ownership whenever possible.

## Legal activation

Before relying on the Square Contract templates for paid clients, finalize the ownership/offboarding, refund, failed-payment, cancellation, and scope policies and have a California-qualified attorney review the client service agreement and public Terms.
