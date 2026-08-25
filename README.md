# SmartGP — clickable prototype

A working front-end prototype of the SmartGP patient journey, patient account and admin back office, built from the Business and Functional Requirements Document and the shared website content outline.

The point of this build is **flow**: what a patient clicks, in what order, what the system does at each point, and where SmartGP hands over to SmartRx. It is not the production Laravel application.

---

## Run it

No build step, no dependencies, no server required.

```bash
git clone https://github.com/NupoorsCode/SmartGP.git
cd SmartGP
open index.html          # macOS
# or: start index.html    (Windows) / xdg-open index.html (Linux)
```

To publish it for the client to click through: **Settings → Pages → Deploy from branch → `main` / root**. It runs as-is on GitHub Pages because everything is static and routing is hash-based.

A single-file version is also included (`SmartGP-preview.html`) for emailing to people who will not clone a repo. Regenerate it after changes with `python3 build.py`.

---

## Files

```
index.html              app shell — header, nav, footer, modal, toast
build.py                inlines everything into SmartGP-preview.html
assets/css/styles.css   the whole design system, one file
assets/js/data.js       content, catalogue, questionnaire schema  ← edit this first
assets/js/core.js       store, hash router, form engine, chrome
assets/js/site.js       public pages
assets/js/journey.js    the 13-step consultation flow and booking
assets/js/account.js    patient dashboard, repeat check-in, side effects
assets/js/admin.js      back office
assets/js/app.js        route table and boot
docs/FLOW.md            every route, every decision point, in writing
```

`data.js` is the file to change when the clinical content arrives. Questions, options, help text, flags, prices and strengths are all data — nothing about the questionnaire is written into code, which is the same structural decision the requirements document calls for.

---

## What actually works

**Patient journey** — age gate (blocks under 18 and over 75 with signposting), treatment status, treatment selection, treatment information, expectation setting, common preliminary questions with UK postcode lookup, height/weight with live BMI and a comorbidity checklist that appears only in the 25–30 band, consent and ID upload, weight verification choice, a treatment-specific safety screen that changes with the treatment chosen, GP practice search and consent, check-your-answers, per-treatment cautions, account creation, submission, slot picker, confirmation with safety netting.

**Dynamic flow** — pregnancy questions are not shown to a patient who recorded male sex at birth; dose questions appear only for someone already on a GLP-1; delivery address appears only if it differs. `showIf` on any field drives this.

**Flagging, not deciding** — an exclusion answer is highlighted at the top of the clinician's view of the submission and is never shown to the patient as a refusal. There is no code path anywhere in this build that approves, rejects or triages a patient.

**Booking** — clinic-defined duration, buffer, lead time, horizon, working days and closures; slots generated from those parameters; no clinician shown to the patient; slot held on selection; email and SMS confirmation simulated.

**Patient account** — appointments with reschedule and cancel, most recent order with the four SmartRx status stages, repeat prescription check-in, side effect report with Yellow Card signposting, communication preferences, data rights.

**Admin** — dashboard, submission view with flags and identity document access, outcome recording that notifies the patient and creates an order, patient search, diary and booking rules, product and price management with availability flags, service builder with publication gated on recorded clinical sign-off, questionnaire builder that adds a live question to the patient journey, notifications, users and roles, clinical governance reporting, and an audit log that fills up as you click.

**Compliance behaviour you can test**
- Try to attach a promotion to Mounjaro in *Products and prices* — blocked at the data layer, and the attempt is logged.
- Try to publish a new service before its questionnaire is signed off — blocked, with the sign-off route offered.
- Switch the role selector to Finance and open *Questionnaires* — refused.
- Flag a strength unavailable and it disappears from the patient's choices immediately.
- Everything above shows up in *Audit log*.

**Start here:** open `#/flow` in the running site. It is the whole click-through map, and every box is a link into that screen.

---

## What is deliberately faked

| Faked | Why, and what replaces it |
|---|---|
| Authentication | Log in with anything. Real build: Laravel auth, email verification, two-step login for staff. |
| Persistence | In-memory only — refreshing resets everything. Real build: MySQL. |
| Postcode and GP lookup | Returns fixed results. Real build: UK address service and NHS organisation data. |
| File upload | Reads the filename only. Real build: encrypted private storage, signed links, 30-day deletion job. |
| Email and SMS | Toasts and notices. Real build: queued Laravel notifications. |
| Video consultation | Not built and never will be — it stays on the clinic's existing platform. |
| Prescribing, payment, dispensing | Out of scope. SmartRx. |
| Prices and product data | Indicative. Must be confirmed clinically and commercially before publication. |

---

## Design notes

Fraunces for display, Public Sans for body, IBM Plex Mono for references, times and system data. Palette carried from SmartRx: pine ink, clinic teal, mint surface. Generous whitespace, one call to action per screen, no urgency devices, no before-and-after imagery, no outcome claims — restraint here is a regulatory requirement as much as a design preference.

The one deliberate flourish is the **journey rail**: a persistent spine down the left of the consultation that shows all thirteen stages, marks the two that branch by treatment, and lets a patient jump back to anything they have already passed. It makes the shape of the flow visible while you are inside it.

Accessibility: visible labels on every field, error messages that say what to fix, keyboard operable throughout, visible focus, reduced motion respected.

---

## Still open

Four decisions from the requirements document affect what gets built next, and three of them touch this prototype directly:

1. **Booking architecture (DEC-01)** — the slot picker here manages its own diary. If SmartGP writes into Microsoft calendars instead, the generation logic in `buildSlots()` changes.
2. **PMR integration (DEC-02)** — the admin submission view is the stand-in. How the submission actually reaches the clinician, and how the outcome returns, is not decided.
3. **CQC registration (DEC-03)** — longest lead time in the project. The footer carries a placeholder.
4. **Standalone consultation (DEC-04)** — built in as the advice-only service, with the hosted payment step shown at booking. Remove it and SmartGP needs no payment capability at all.
