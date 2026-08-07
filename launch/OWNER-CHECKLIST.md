# OneTap Creative — Owner Checklist to 100%

This is the owner-side checklist for items that require account ownership, identity verification, payment authorization, legal approval, or a real-client action. The website/code items are handled separately by the repository launch audit.

## Launch gate — complete before broad paid advertising

### 1. Professional business email
- [ ] Create `hello@onetapcreative.com` with your chosen email provider.
- [ ] Add the provider's current SPF record in DNS.
- [ ] Add the provider's DKIM record(s) in DNS.
- [ ] Add a DMARC record. Start with the provider's recommended monitoring policy if you are unsure.
- [ ] Send a test from `hello@onetapcreative.com` to Gmail.
- [ ] Send a test from `hello@onetapcreative.com` to Outlook/Hotmail.
- [ ] Reply from both test inboxes and confirm replies arrive.
- [ ] Confirm the messages are not landing in spam.
- [ ] After the mailbox passes, ask the OneTap agent to migrate both website forms to the professional mailbox and re-test the secure FormSubmit route.

### 2. Square recurring billing
- [ ] In Square, create **OneTap Creative Complete Online Presence Plan**.
- [ ] Set the recurring amount to **$179 monthly**.
- [ ] Turn tipping off.
- [ ] Collect client name, business name, and email at checkout when supported.
- [ ] Keep the public homepage as inquiry-only; do not place the payment link on the homepage.
- [ ] Use the signed agreement to define the three-month minimum; the payment link by itself does not replace the contract.
- [ ] Complete one $179 test transaction or approved test-mode checkout.
- [ ] Confirm the client receipt is clear and branded.
- [ ] Confirm you know how to handle a failed payment, card update, cancellation, and refund request.

### 3. Google Search Console
- [ ] Create/verify a **Domain property** for `onetapcreative.com`.
- [ ] Complete the DNS TXT verification at the domain registrar.
- [ ] Submit `https://onetapcreative.com/sitemap.xml`.
- [ ] Inspect `https://onetapcreative.com/` in URL Inspection.
- [ ] Request indexing if Google has not indexed the homepage yet.
- [ ] Confirm there are no manual actions or security issues.
- [ ] Record the starting baseline: indexed pages, impressions, clicks, CTR, and top queries.

### 4. Analytics and conversions
- [ ] Enable Vercel Web Analytics for the production project.
- [ ] Create a GA4 property for OneTap Creative if you plan to run marketing/ads or want detailed conversion reporting.
- [ ] Add the GA4 Measurement ID to the production site through the OneTap agent after the property exists.
- [ ] Verify a live page view in GA4 Realtime.
- [ ] Submit one test lead and confirm the `generate_lead` / OneTap lead events are received.
- [ ] Confirm UTM source, medium, campaign, and content are captured in a test request.

### 5. Google Business Profile decision
- [ ] Confirm OneTap Creative currently meets Google's Business Profile eligibility requirements before creating a profile.
- [ ] If eligible, create the profile using truthful public business information.
- [ ] Complete Google's required verification yourself.
- [ ] Add the production website, service area, services, hours, logo, and approved business photos.
- [ ] If OneTap is not currently eligible, skip creation rather than risking a suspension; Search Console and organic website SEO can still operate without a OneTap Business Profile.

### 6. Legal/business approval
- [ ] Review the `client-operations/CLIENT-OPERATIONS-KIT.md` agreement and scope template.
- [ ] Decide the final website/domain ownership and offboarding/buyout policy.
- [ ] Decide the failed-payment grace period and suspension policy you will actually enforce.
- [ ] Decide the refund policy you will actually enforce.
- [ ] Have a California-qualified attorney review the final client service agreement and public Terms before relying on them for paid clients.
- [ ] Save the approved agreement as the only version used for new clients.

### 7. End-to-end mock client test
- [ ] Use a separate test email and fictional business.
- [ ] Complete every item in `launch/MOCK-CLIENT-TEST.md` from a phone.
- [ ] Confirm public request email delivery.
- [ ] Confirm automatic prospect response.
- [ ] Confirm Reply-To opens the prospect's email address.
- [ ] Confirm the thank-you page loads.
- [ ] Complete the agreement/scope step.
- [ ] Complete the Square payment step.
- [ ] Complete mobile onboarding with small image/PDF uploads.
- [ ] Confirm onboarding email and attachments arrive.
- [ ] Confirm onboarding success page loads and saved form data clears.
- [ ] Do not begin broad paid advertising until this full test passes.

## Client-conversion proof — strongly recommended before scaling outreach

### 8. Testimonials and permissions
- [ ] Ask DJ JRV for a short written testimonial about the website/build experience.
- [ ] Get permission to display the testimonial, business name, and website link on OneTap Creative.
- [ ] Ask Freda for a testimonial once the project is fully approved/ready.
- [ ] Only publish real reviews/testimonials; never use placeholder ratings as customer proof.
- [ ] Ask satisfied clients for a Google review only if OneTap has an eligible verified Business Profile.

### 9. Portfolio confirmation
- [ ] Confirm DJ JRV is okay with OneTap featuring the live site as a client case study.
- [ ] Confirm Freda is okay with OneTap featuring the live site as a client case study.
- [ ] Tell the OneTap agent immediately if a client asks for their project, name, images, or testimonial to be removed.

### 10. Domain and production account ownership
- [ ] Confirm `onetapcreative.com` auto-renew is enabled at the registrar.
- [ ] Confirm the registrar account has two-factor authentication enabled.
- [ ] Confirm the Vercel account/project has two-factor authentication enabled where available.
- [ ] Confirm the production domain resolves to the intended Vercel project.
- [ ] Confirm `https://onetapcreative.com/robots.txt` loads.
- [ ] Confirm `https://onetapcreative.com/sitemap.xml` loads.
- [ ] Confirm `https://onetapcreative.com/404.html` loads.

## Operating discipline after launch

### 11. Lead response process
- [ ] Check new leads at least once each business day.
- [ ] Target a reply within one business day as promised on the website.
- [ ] Add each real lead to `client-operations/LEAD-TRACKER.csv` or your future CRM.
- [ ] Track lead source, discovery call, proposal, agreement, payment, onboarding, and status.

### 12. Monthly client care
- [ ] Test each client's primary form/booking/call/text path monthly.
- [ ] Check domain, HTTPS, broken links, and mobile navigation.
- [ ] Review Search Console indexing, clicks, impressions, top queries, and Core Web Vitals.
- [ ] Review the client's Google Business Profile status where applicable.
- [ ] Record client update minutes used out of the included 30 minutes.
- [ ] Send or retain a simple monthly care summary and one recommended next action.

## 100% definition

OneTap Creative is **website-launch complete** when the repository audit passes and sections 1–7 above are complete. It is **client-acquisition ready at full strength** when sections 8–10 are also complete. Sections 11–12 are ongoing operating requirements rather than one-time launch tasks.
