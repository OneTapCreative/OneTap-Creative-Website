# OneTap Creative Mobile Client Onboarding Portal

Private route: `/onboarding/`

## When to send the portal

Send the onboarding link only after:

1. The project has been qualified.
2. The client agreement has been signed.
3. The first $179 monthly payment has been completed.
4. The client has been told that the first payment starts the three-month commitment.

The public OneTap website does not link to this route. The page is marked `noindex` and the repository robots file blocks crawler access.

## Client-facing flow

1. Welcome and agreement/payment confirmation
2. Business information
3. Primary website goal
4. Services and pricing
5. Brand and visual direction
6. Photos and content
7. Customer contact setup
8. Google Business Profile status
9. Final review and submission

The old domain/account section is intentionally excluded. OneTap Creative provides and connects the domain and creates the website.

## Mobile experience

- One question group per screen
- Large tap targets
- Sticky Back and Continue controls
- Automatic text-answer saving through browser local storage
- Save-and-finish-later option on the same device and browser
- Conditional questions based on customer action and Google Business Profile status
- Phone photo uploads with previews
- 20 MB total upload limit
- Review summary with edit buttons
- Accessible required-field validation
- Completion page with next steps

## Important limitation

Text answers save locally on the client’s current browser. Selected files are not permanently saved between devices or after browser data is cleared. The portal tells clients they may need to select files again if they leave before submitting.

## Form delivery

The portal currently submits through the same FormSubmit destination used by the public OneTap request form:

`codicta@gmail.com`

After a professional OneTap mailbox is activated and tested, update the form action in `onboarding/index.html`.

The form submits as `multipart/form-data` so the selected attachments can be delivered with the onboarding response.

## Personalized links

The portal supports optional prefilled business name and email query parameters:

`https://onetapcreative.com/onboarding/?business=Business%20Name&email=client@example.com`

Do not place sensitive information or passwords in the URL.

## Security rules

- Never request or accept passwords through this portal.
- The client owns the Google Business Profile.
- OneTap receives manager access only.
- Do not publicly post a client-specific onboarding link.
- Do not treat `noindex` as authentication; this is a private-link workflow, not a secure account portal.
- For cross-device saving, secure uploads, user accounts, or a true client dashboard, replace the static form workflow with an authenticated backend and protected storage.

## QA checklist

Before sharing the production link:

- Test all eight steps on a phone.
- Confirm progress saving and restoration.
- Confirm business/service-area conditional fields.
- Test every website-goal condition.
- Test Yes/No/Not Sure Google Business Profile paths.
- Submit a full test with small attachments.
- Confirm the email arrives with the correct subject and attachments.
- Confirm the success page loads.
- Confirm saved answers clear after success.
- Confirm no passwords or domain-purchase questions appear.
