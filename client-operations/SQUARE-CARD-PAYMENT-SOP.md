# OneTap Creative — Square Recurring Payment Link SOP

Current launch preference: **credit/debit card only**.

The signed Square Contract controls the three-month minimum, cancellation terms, and scope. Square handles the recurring payment. The public OneTap homepage remains inquiry-only.

## Client payment journey

Lead → discovery → recommend Start or Grow → matching Square Contract → client signs → verify completed in Square → private Square recurring payment link → first credit/debit card payment → automatic monthly billing → onboarding.

Create **two reusable private links**:
- OneTap Start — $99/month
- OneTap Grow — $149/month

Do not place either Square link on the public homepage.

## Global Square Payment Link settings

In Square Dashboard go to **Payments & orders → Payment links → Settings → General**.

For the current OneTap launch workflow:
- Card payments: accepted automatically by Square Payment Links
- Apple Pay: Off
- Google Pay: Off
- Cash App Pay: Off
- Tipping: Off
- Afterpay online: Off in Square payment-method settings if you want strict card/debit-only checkout
- Customer notes: Optional
- Email transaction notifications: On
- Branding: Add OneTap logo/business name when available

Square payment-link wallet settings are global to Payment Links, so review them before sending a live client link.

## OneTap Start recurring link

Create link → **Collect a payment**

- Title: **OneTap Start — Monthly Website Service**
- Amount: **$99.00**
- Frequency: **Recurring**
- Recurrence: **Monthly**
- End date: **No automatic end date**
- Description:

**Managed OneTap Creative website service for a local service business. Includes a custom mobile-friendly website, hosting, SSL, backups, SEO essentials, two organized prelaunch revision rounds, up to 15 minutes of monthly updates, maintenance, and support. Three-month minimum applies under the signed client agreement; after the minimum, service continues month-to-month with 30 days’ written notice.**

Custom fields:
1. **Business Name**
2. **Agreement Signer Name**

Advanced settings:
- Tipping: Off
- Redirect after checkout:  
  **https://one-tap-creative-website-git-main-clarenceworkflows-projects.vercel.app/onboarding/?plan=start**

## OneTap Grow recurring link

Create link → **Collect a payment**

- Title: **OneTap Grow — Monthly Website + Google Visibility**
- Amount: **$149.00**
- Frequency: **Recurring**
- Recurrence: **Monthly**
- End date: **No automatic end date**
- Description:

**OneTap Creative managed website service with advanced search support. Includes everything in OneTap Start plus Google Business Profile assistance, advanced SEO foundation, local keyword mapping, Google Search Console, structured data/local-search alignment, basic ongoing search-health checks, and up to 30 minutes of monthly updates. Three-month minimum applies under the signed client agreement; after the minimum, service continues month-to-month with 30 days’ written notice.**

Custom fields:
1. **Business Name**
2. **Agreement Signer Name**

Advanced settings:
- Tipping: Off
- Redirect after checkout:  
  **https://one-tap-creative-website-git-main-clarenceworkflows-projects.vercel.app/onboarding/?plan=grow**

## Why the links stay private

The payment links are reusable, but they should only be sent after OneTap has:
1. Reviewed the lead.
2. Completed discovery.
3. Recommended Start or Grow.
4. Received the signed client agreement.

The signed Square Contract—not the payment link—defines the three-month minimum and the client-specific scope.

## Payment message to client

**Your OneTap agreement is complete.**

Use the secure Square link below to activate your **[OneTap Start / OneTap Grow]** plan:

**[SQUARE PAYMENT LINK]**

Your plan is **[$99 / $149] per month** with the initial three-month commitment described in your signed agreement.

After successful payment, Square will send you directly to OneTap onboarding so we can begin collecting the information needed for your website.

Never send card information by email or text.

## Matching payment to the agreement

Before production starts, confirm:
- payment amount matches selected plan;
- Business Name matches the signed agreement;
- Agreement Signer Name matches the submitted agreement;
- first payment shows successful in Square.

Then proceed with onboarding/production.

## Failed recurring payment workflow

### Day 0 — payment fails
Send:

**Your OneTap Creative monthly payment did not go through.**

Please update your payment method through Square so we can keep your service current. If you have already corrected the payment, no further action is needed.

### Day 3 — reminder
Send:

**Quick billing reminder from OneTap Creative:** your monthly payment is still showing as unpaid. Please update your payment method through Square. If you need help locating the payment update, reply and we’ll point you in the right direction.

### Day 7 — grace-period notice
Send:

**Your OneTap Creative account is now past the standard payment grace period.** Please resolve the Square payment to avoid interruption of hosting, maintenance, or support.

### Day 14 — suspension
If permitted by the signed agreement:
- send written suspension notice;
- suspend hosting/support only after notice;
- do not delete client files or domain records as part of the initial suspension;
- restore service after the outstanding balance is resolved.

## Cancellation

- The three-month minimum is controlled by the signed agreement.
- After the minimum, require 30 days’ written notice.
- End/cancel the Square subscription only after confirming the contractual cancellation date.
- Send written confirmation of the final billing date.

## Refunds

Do not promise automatic refunds. Follow the signed agreement and documented OneTap refund policy.

## Test before first real client

- Create Start recurring payment link
- Verify $99 monthly
- Verify custom fields
- Verify card/debit-only settings
- Verify tipping is off
- Complete a test payment if Square provides an appropriate test method
- Verify redirect selects Start on onboarding
- Repeat for Grow at $149
- Verify redirect selects Grow on onboarding
- Confirm receipts and Square reporting identify the client correctly
