# External Account Activation

These actions require the business owner's account access, identity verification, DNS control, payment authorization, or legal approval. Complete them with `launch/OWNER-CHECKLIST.md`.

## Professional email

Planned mailbox: `hello@onetapcreative.com`.

1. Create and verify the mailbox.
2. Configure the email provider's current SPF, DKIM, and DMARC DNS records.
3. Test sending to Gmail and Outlook/Hotmail.
4. Reply from both test accounts and confirm delivery is not going to spam.
5. After the mailbox passes, migrate **both** secure FormSubmit routes together and reactivate/test the new route before retiring the current verified delivery route.

Do not expose a personal inbox in public HTML, JavaScript, or client-facing documentation.

## Square recurring payment

Create **OneTap Creative Complete Online Presence Plan** at **$179 monthly**. The signed agreement—not the payment link by itself—defines the three-month minimum.

- Disable tipping.
- Collect client name, business name, and email where supported.
- Test checkout/receipt behavior.
- Confirm failed-payment, card-update, cancellation, and refund handling.
- Keep the public homepage inquiry-only; send payment only after fit/scope/agreement approval.
- Send the personalized onboarding URL only after payment is confirmed.

## Analytics

The website already records UTM values, CTA clicks, portfolio clicks, lead submission events, and `generate_lead` hooks.

- Enable Vercel Web Analytics for baseline traffic measurement.
- Create GA4 if detailed marketing attribution/conversion reporting is needed.
- Add the production GA4 Measurement ID only after the real property exists.
- Verify page views and a test `generate_lead` event in production before paid advertising.

## Search Console

- Verify the `onetapcreative.com` **Domain property** using DNS.
- Submit `https://onetapcreative.com/sitemap.xml`.
- Inspect the homepage and request indexing if needed.
- Check manual actions and security issues.
- Record the starting clicks, impressions, CTR, indexed pages, and top queries.

## Google Business Profile

Create a OneTap Creative Google Business Profile only if the business currently meets Google's eligibility requirements. Use truthful public business information and complete required verification through the owner's account. Do not create an ineligible or misleading profile simply for SEO.

Client Business Profiles remain **client-owned**. OneTap should receive Manager access rather than taking primary ownership whenever possible.

## Legal activation

Before relying on the agreement for paid clients, finalize the ownership/offboarding, refund, failed-payment, cancellation, and scope policies and have a California-qualified attorney review the client service agreement and public Terms.
