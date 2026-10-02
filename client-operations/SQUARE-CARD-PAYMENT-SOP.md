# OneTap Creative — Square Card Payment SOP

Current launch preference: **credit/debit card only**.

This is the operating setup for OneTap Creative recurring client billing. The signed client agreement controls the three-month minimum, cancellation terms, and scope. Square is the payment processor, not the contract.

## Client payment journey

Lead → discovery → recommend Start or Grow → signed agreement → private Square recurring invoice → first credit/debit card payment → card saved on file with customer consent → onboarding → monthly automatic billing.

Do not place a public Square checkout link on the homepage.

## Square items

### OneTap Start
- Item name: **OneTap Start**
- Price: **$99.00**
- Billing: **Monthly**
- Category: Website Services
- Description: **Managed professional website for a local service business, including hosting, SSL, maintenance, SEO essentials, founder-led support, and the included monthly update allowance.**
- First payment: Due before onboarding
- Initial minimum: 3 months / $297 total under signed agreement
- After minimum: Month-to-month with 30 days' written notice under signed agreement

### OneTap Grow
- Item name: **OneTap Grow**
- Price: **$149.00**
- Billing: **Monthly**
- Category: Website Services
- Description: **Everything in OneTap Start plus Google Business Profile assistance, advanced SEO foundation, local keyword mapping, Search Console, schema/local search alignment, and the included monthly update allowance.**
- First payment: Due before onboarding
- Initial minimum: 3 months / $447 total under signed agreement
- After minimum: Month-to-month with 30 days' written notice under signed agreement

## Square recurring invoice settings

Create one recurring invoice series per client after the agreement is signed.

Recommended settings:
- Frequency: Every 1 month
- Start date: Date the first payment is due
- End date: No automatic end date
- Payment method: Credit/debit card
- Save card on file: Enabled / customer consent required
- Automatic card charge: Enabled after card is stored
- Tipping: Off
- ACH / bank transfer: Do not enable for the current launch workflow
- Afterpay: Off
- Cash App Pay: Do not use for the recurring OneTap workflow
- Gift cards: Do not use for the recurring OneTap workflow
- Customer record: Full name, business name, email, phone
- Invoice delivery: Email
- Receipt delivery: Email
- Internal customer note: Selected plan + agreement date + minimum-term end date

If Square presents additional payment methods by default, review **Accepted payment methods** on the invoice/template and leave only the card options needed for the OneTap launch workflow.

## Invoice title

**OneTap Creative — [Start/Grow] Monthly Service**

## First invoice message

Thank you for choosing OneTap Creative.

This invoice activates your selected monthly service after your signed agreement. Your first payment starts the three-month minimum commitment. Once payment is confirmed, we will send your onboarding link and begin the website process.

Your card may be securely saved with Square for automatic monthly billing when you authorize Card on File.

Questions about your scope or billing? Reply before submitting payment.

## Monthly invoice description

**OneTap Creative [Start/Grow] — Monthly managed website service for [BUSINESS NAME].**

## Payment confirmation message

**Payment received — welcome to OneTap Creative.**

Your [Start/Grow] plan is active. The next step is onboarding. Complete the onboarding information so we can begin or continue your website work.

## Card authorization rule

The client must authorize Square to save and charge the card on file. OneTap never stores card numbers, CVV, or other raw payment credentials outside Square.

## Failed payment workflow

Square does not automatically reprocess a declined recurring card charge. Use this sequence:

### Day 0 — payment declined
- Confirm Square sent the decline notice.
- Send OneTap failed-payment message.
- Keep website/service active during the grace period.

Message:

**Your OneTap Creative payment did not go through.**

Please update your payment method through the secure Square invoice so we can keep your service current. If you already updated it, no further action is needed.

### Day 3 — reminder
Message:

**Quick billing reminder from OneTap Creative:** your monthly payment is still showing as unpaid. Please update your card through the secure Square invoice. If you need help, reply and we’ll point you in the right direction.

### Day 7 — grace-period notice
Message:

**Your OneTap Creative account is now past the standard payment grace period.** Please update the payment method through Square to avoid interruption of hosting, maintenance, or support.

### Day 14 — suspension
If the signed agreement and OneTap policy permit:
- Send written suspension notice.
- Suspend hosting/support only after the notice is sent.
- Do not delete client files or domain records as part of an initial suspension.
- Restore service after the outstanding balance is paid.

## Card update process

When the client changes cards:
1. Have the client use the secure Square invoice/payment page to update the saved card where available.
2. Confirm the recurring invoice series points to the correct Card on File.
3. Never ask the client to email or text a full card number or CVV.

## Cancellation

- Three-month minimum is controlled by the signed agreement.
- After the minimum, require 30 days' written notice.
- End the recurring Square series only after confirming the contractual cancellation date.
- Send written confirmation of the final billing date.

## Refunds

Do not promise automatic refunds. Follow the signed agreement and documented OneTap refund policy. Keep a written record of any approved refund and the reason.

## Test before first real client

- Create test customer
- Create Start recurring series
- Confirm $99 amount and invoice description
- Confirm only intended card payment methods are presented
- Confirm tipping is off
- Confirm card-save/authorization language
- Complete approved test-mode or low-risk test
- Confirm receipt
- Confirm onboarding is sent only after payment
- Repeat for Grow at $149
- Test a card update
- Review how Square surfaces a declined recurring payment
