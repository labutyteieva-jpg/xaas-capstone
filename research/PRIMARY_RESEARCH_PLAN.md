# Primary research plan & interview guide

**Date:** 2026-06-15
**Why this exists:** the Capstone requires *primary data analysis* — designing a study, collecting
data, and analysing it. Secondary data (the Eurostat/Comtrade work) does not satisfy that bar on
its own. This document is the study design plus the instruments, written so the team can start
collecting data before the midterm. The midterm bar is "real progress, not ideas," so the concrete
goal before end-June is: finalise this guide + consent, recruit, and run the first 2–3 interviews.

---

## 1. What the primary research must answer

These are the **business/market** research questions (distinct from the technical evaluation RQ in
`docs/DEEPTECH_PLAN.md`, but feeding the same project):

- **PRQ1 — Current process:** How do Lithuanian/EU SME exporters *without* an in-house export team
  actually make export decisions today (market selection, logistics, customs/compliance)?
- **PRQ2 — Pain:** Which export tasks cost the most time, money, or risk, and where does the
  process break?
- **PRQ3 — Concept fit & trust:** How do they react to an orchestration-based export-decision tool,
  and — critically — what would have to be true for them to *trust* an AI recommendation,
  especially on compliance?
- **PRQ4 — Willingness to pay:** Is there a credible willingness to pay, and under which model
  (subscription / per-transaction / per-service)?

**Maps to the proposal's "assumptions to verify":** SMB adoption of a subscription XaaS model
(PRQ4), market demand exists (PRQ1–PRQ3). *API/technical feasibility is not an interview question —
it is tested in the build phase.*

---

## 2. Method and why it's justified

**Two strands + an optional third:**

1. **Semi-structured interviews (primary, qualitative).** Best fit for exploratory understanding of
   a *process* and for capturing unanticipated pain points and trust concerns; the semi-structured
   format lets the interviewer probe. A survey alone cannot surface *why*.
2. **Short structured survey (secondary, breadth).** Quantifies how common the pain points are and
   gives a defensible willingness-to-pay signal across a wider sample.
3. **Pilot case studies (later phase).** 3 SMEs trial the tool on real/simulated scenarios — the
   strongest evidence of real (not stated) demand. Out of scope until the build exists.

**Sample (interviews):** target **n ≈ 10–12**. This is for *qualitative saturation*, **not**
statistical generalisation — say this explicitly. Purposive sampling:
- Lithuanian/EU product exporters, < 250 employees, with **no or limited in-house export function**;
- a mix of currently-exporting and aspiring-to-export firms;
- weighted toward **manufacturing / machinery** first (the largest verified export sectors), with
  some spread across other sectors;
- optionally 2–3 **export-service experts** (a freight forwarder, a customs broker) for
  triangulation — they see many SMEs' problems at once.

**Recruitment channels (confirm/fill in what you actually have access to):** Enterprise Lithuania /
LVPA, chambers of commerce, sector associations, Ieva's sales network, targeted LinkedIn outreach,
and snowball referrals from each interviewee. **Note the selection-bias risk** — firms that agree to
talk about export problems may not represent those who avoid exporting entirely.

**Survey sample:** non-probability (convenience + the channels above) → analyse **descriptively
only**; do not infer population proportions.

**Ethics / consent (EU → GDPR applies):** obtain informed consent before recording; explain purpose,
how data is stored and anonymised, and the right to withdraw; anonymise transcripts; keep recordings
in a controlled location and delete per a stated retention period. A short consent script is in §6.

---

## 3. Interview guide (semi-structured, ~45 min)

**Design principle (state this in the methodology):** *discovery before concept.* Phases 1–3 do
**not** mention the product, so pain points are captured without priming. The concept is only
introduced in Phase 4. Questions are open; avoid yes/no and leading phrasing ("Don't you think X is
a problem?" → instead "How do you handle X?").

**Phase 0 — Intro & consent (3 min).** Thanks; purpose; consent + recording permission; reassure
there are no right answers; confirm role and that they're involved in export decisions.

**Phase 1 — Current export process (10 min).** *No product mention.*
- "Walk me through the last time your company entered, or seriously considered, a new export market."
- Probes: How did you decide *which* market? Who was involved? How did you handle logistics? How did
  you handle customs/compliance and documentation? What tools or outside help did you use? Roughly
  how long did it take?

**Phase 2 — Pain points (10 min).** *No product mention.*
- "Which part of exporting is the most difficult or time-consuming for you?"
- "Tell me about a time an export didn't go to plan — what happened?"
- Probes: cost, delays, compliance errors, lack of expertise, fragmented tools. Let them rank.

**Phase 3 — Current solutions (5 min).**
- "What do you use today to manage these things — people, services, software?"
- "What's missing from what's available?"

**Phase 4 — Concept reaction (10 min).** *Introduce the concept neutrally and briefly* (one or two
sentences; avoid selling): "Some teams are exploring a single tool that suggests target markets,
estimates logistics cost/time, and flags compliance requirements, coordinating several specialised
components behind one interface."
- "What's your honest first reaction?"
- "What would worry you about using something like that?"
- **Trust probe (key):** "It would make recommendations, including on compliance. What would have to
  be true for you to trust those — particularly the compliance parts?" *(This directly informs the
  verification-step argument in the deep-tech plan.)*

**Phase 5 — Willingness to pay (5 min).** *Anchor on current spend first* (more reliable than a bare
"would you pay?"):
- "Roughly what do you spend today — money and people's time — on the tasks we discussed?"
- Then gauge reaction to a subscription vs per-transaction vs per-service model, and which fits how
  they budget. Keep this qualitative; the survey (§4) does the structured price test.

**Phase 6 — Wrap (2 min).** "Anything important about exporting we didn't ask about?" Ask for
referrals (snowball) and permission to follow up for the later pilot.

---

## 4. Survey structure (5–8 min, online)

1. **Screening:** Do you make/influence export decisions? Does your firm export or plan to? (filter)
2. **Firm profile:** size band, sector, current export markets, in-house export team (Y/N).
3. **Pain frequency & severity:** Likert (1–5) across market selection, logistics, customs/
   compliance, documentation, payments/FX.
4. **Current tools & spend:** what they use; approximate annual spend / time on these tasks.
5. **Concept interest:** brief neutral description → interest Likert + one open "biggest concern".
6. **Willingness to pay — use a real method, not a single question.** Recommend the **Van Westendorp
   Price Sensitivity Meter** (four questions: at what monthly price would this be *too cheap to
   trust / a bargain / getting expensive / too expensive to consider*). This yields a defensible
   acceptable-price range and is far more credible to a panel than "would you pay €X?". (Gabor–Granger
   is an acceptable alternative.) **Justify this choice in the methodology** — it shows you know
   stated WTP is weak evidence and chose an instrument that mitigates it.
7. **Optional:** contact details to join the pilot.

---

## 5. Analysis plan

- **Interviews:** record (with consent) → transcribe → **thematic analysis** (inductive coding;
  build a codebook; group into themes). Report themes with anonymised illustrative quotes, and tie
  each back to PRQ1–PRQ4 and the proposal's assumptions. Tooling: spreadsheet/NVivo/manual is fine
  at this scale.
- **Survey:** descriptive statistics; rank pain points; compute the Van Westendorp acceptable-price
  range and optimal price point; cross-tab by firm size/sector **with an explicit small-n caveat**.
- **Triangulation:** converge interviews + survey + the secondary Eurostat underserved-markets
  finding. Convergent signals across all three are the strongest claim you can make at this stage.

---

## 6. Consent script (short)

> "Thank you for your time. I'm a VU Business School student researching how small and medium
> exporters make export decisions, for a Capstone project. This will take about 45 minutes. With
> your permission I'd like to record it so I can transcribe accurately; the recording is used only
> for this research, your responses will be anonymised, and you can stop or skip any question at any
> time. May I record? Do you have any questions before we start?"

---

## 7. Honest limitations (state these in the report)

- Small, non-probability sample → **qualitative insight and directional signal only, not
  statistical generalisation.** Do not report interview counts as if they were population shares.
- **Stated** willingness to pay ≠ actual purchasing behaviour; treat as directional. The pilot is
  the stronger demand test.
- Concept reactions are subject to politeness/acquiescence bias; the discovery-before-concept
  ordering and neutral wording mitigate but don't remove this.
- Recruitment/selection bias (firms willing to discuss export problems may differ systematically).

---

## 8. Timeline & midterm deliverable

- **Before end-June (midterm):** finalise this guide + consent; confirm recruitment channels;
  recruit; **run 2–3 interviews**; have the design documented (this file). That is demonstrable
  "real progress."
- **Jul–Sep:** complete ~10–12 interviews + run the survey.
- **Oct–Nov:** pilot case studies (needs the build) + full analysis.
- **Nov–Dec:** write-up and defence.

**Midterm talking point:**
> "Our primary research is designed and underway: ~10–12 semi-structured interviews with LT/EU SME
> exporters plus a survey using a Van Westendorp price test, structured discovery-before-concept to
> avoid priming, analysed thematically and triangulated against our Eurostat findings. We've
> completed the first [N] interviews; early themes are [...]."
