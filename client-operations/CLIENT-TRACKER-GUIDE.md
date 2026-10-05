# OneTap Creative Client Tracker Guide

Use `LEAD-TRACKER.csv` as the single operational tracker from first inquiry through monthly care.

## Core rule

Every active row should always have:

- **Client Status**
- **Next Action**
- **Owner Deadline**

If any of those three are blank, the client can become easy to lose track of.

## Recommended field values

### Discovery Status
- Not scheduled
- Scheduled
- Complete
- Not needed

### Recommended Plan
- OneTap Start — $99/month
- OneTap Grow — $149/month
- Undecided

### Agreement Status
- Not sent
- Sent
- Signed
- Needs revision
- Declined

### First Payment Status
- Not sent
- Pending
- Paid
- Failed
- Refunded

### Onboarding Status
- Not sent
- Sent
- Received
- Needs information
- Complete

### Client Status
Use these exact stages:

- Prospect
- Follow-Up
- Discovery Complete
- Agreement Sent
- Awaiting Payment
- Onboarding Sent
- Onboarding Received
- Waiting on Client
- Ready to Build
- Build in Progress
- Client Review — Round 1
- Revision — Round 2
- Approved for Launch
- Live — Monthly Care
- Paused — Payment / Client
- Closed / Canceled

### GBP Status (Grow Only)
For Start clients use **N/A**.

For Grow clients use:
- Not reviewed
- Existing verified profile
- Manager access pending
- Ownership pending
- Setup needed
- Verification pending
- Optimization in progress
- Active / optimized
- Ineligible

## How to use dates

- **Follow-Up Date:** next sales follow-up before the client activates.
- **Owner Deadline:** next date OneTap must take action.
- **First Review Due:** target 7–10 business days after all required website content is complete.
- **Launch Target:** expected client-facing launch date.
- **Launch Date:** actual live date.
- **Monthly Billing Date:** recurring Square billing date.

## Monthly value

Record:
- Start: **99**
- Grow: **149**

Do not enter the three-month total here. This column represents recurring monthly value.

## Monthly update minutes

- Start allowance: **15 minutes**
- Grow allowance: **30 minutes**

Reset the used-minute count each billing month. Unused time does not roll over.

## Example active-client row logic

A Grow client who has paid and submitted onboarding but is missing photos should look like:

- Agreement Status: Signed
- First Payment Status: Paid
- Onboarding Status: Needs information
- Client Status: Waiting on Client
- Next Action: Receive remaining project photos
- Owner Deadline: next follow-up date
- GBP Status: appropriate Grow status

Once the missing content arrives:

- Onboarding Status: Complete
- Client Status: Ready to Build
- Next Action: Create production brief and begin build
- Owner Deadline: production start date
- First Review Due: 7–10 business days from complete intake

## Weekly owner review

At least once per week:

1. Sort by **Owner Deadline**.
2. Review all overdue actions.
3. Check all **Waiting on Client** rows.
4. Check all failed/pending payments.
5. Check all Grow GBP pending statuses.
6. Check builds approaching **First Review Due**.
7. Check approved sites that have not launched.
8. Review live clients needing monthly care.

The tracker is not just a history log. It is the operating queue for OneTap Creative.
