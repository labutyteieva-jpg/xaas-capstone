# Deep-tech & evaluation plan (architecture-agnostic)

**Date:** 2026-06-15
**Purpose:** Define the Capstone's applied-innovation core and how it will be evaluated, in a
way that does **not** depend on the final software architecture. This is the spine for the
midterm deck and the answer to the panel's hardest question: *where is the deep tech, and how
will you prove it works?*

**Status note:** No software is built before the end-June midterm; the build runs over
summer–autumn (consistent with the proposal's MVP schedule). The midterm is a design-and-evidence
checkpoint, so this plan is what is defended there.

---

## 1. The deep-tech core

The applied-innovation core is an **export-decision orchestration engine**: a system that turns an
SME's product and company profile into ranked, justified export recommendations — target markets,
indicative logistics cost/time, and compliance requirements. The orchestrator decomposes a request
into sub-tasks, routes each to the component best suited to it, and applies a
**verification / reflection step** to high-stakes outputs (above all, compliance) before returning
a result.

**Architecture is deliberately left open.** Whether the components are several LLMs under a
coordinator (pure multi-LLM), or a mix of LLMs for language/reasoning with deterministic
rules/retrieval for compliance and an optimisation routine for logistics (multi-component), is a
**build-phase decision (July–October)**. The research contribution and the evaluation below hold
either way. This is stated explicitly so the midterm does not over-commit to an architecture that
has not yet been prototyped.

---

## 2. Why orchestration (the justification the panel will ask for)

Export decision-making is not one problem but several stitched together:

- **Market/demand estimation** — quantitative; benefits from trade data, not free-text reasoning.
- **Logistics cost and routing** — operational/optimisation; structured computation.
- **Customs / compliance** — rule-heavy, and the *cost of a wrong answer is high*.

A single general-purpose LLM is weakest exactly where it matters most: it can hallucinate
compliance requirements, and it does not natively perform structured cost/route optimisation.
Coordinating specialised components — and **verifying** the high-stakes outputs before they reach
the user — is a plausible route to higher **accuracy and reliability** than one model answering
everything. That plausibility is a hypothesis, not a claim; Section 4 tests it.

**Anti-pattern to avoid:** if "orchestration" collapses into plain prompt-chaining with no
measurable gain over a single model, it is not a research contribution. The evaluation exists to
rule that out (or to honestly report it if true).

---

## 3. Research question and hypotheses

**RQ:** Does an orchestration-based export-recommendation engine produce more **accurate** and
more **reliable** recommendations for Lithuanian SME exporters than a single-LLM baseline?

- **H1 (accuracy):** orchestration performs at least as well as the single-LLM baseline on
  recommendation accuracy.
- **H2 (reliability):** orchestration produces fewer high-severity errors — especially in
  compliance — than the single-LLM baseline.

---

## 4. Evaluation design (this is what makes it *research*, not a product description)

**Task.** Given a product (HS code) + origin (Lithuania) + company profile, output a ranked list
of target markets with indicative cost/time and compliance flags.

**Conditions / baselines.**
- B0 — single general-purpose LLM (the baseline to beat).
- B1 — optional rule-based / heuristic baseline (e.g., rank markets by existing trade gravity).
- T — the orchestration engine (+ verification step).

**Metrics.**
- *Market recommendation:* top-k agreement with a **reference ranking** derived from open trade
  data (Eurostat `ext_tec10`, UN Comtrade) — e.g., do recommended markets align with where
  comparable Lithuanian SMEs actually trade, and with the underserved-market logic from the
  Eurostat analysis already in this repo.
- *Compliance:* precision/recall of compliance flags against a **curated test set** of known
  EU/customs requirements; errors **severity-weighted** (a missed mandatory certificate counts
  more than a minor omission).
- *Reliability:* output consistency across repeated runs; **unsupported-claim (hallucination)
  rate** — share of statements not traceable to a source.

**Data.**
- Market ground-truth/reference: the open datasets already committed (`ext_tec10`, Comtrade).
- Compliance: a small curated set of EU export-compliance rules (built by the team; the honest,
  objective part of the evaluation).
- Perceived usefulness + willingness to pay: SME interviews, survey, and pilots (Section 6).

**Analysis.** Paired comparison across the identical task set; report effect sizes, not just
"it felt better"; include a qualitative error analysis of where each condition fails.

**Honest weakness to disclose at the midterm:** there is **no objective ground truth** for "the
best export market," so the market-recommendation metric is a *proxy* (alignment with revealed
trade patterns and the underserved-market logic). **Compliance is the cleaner, more objective
test** and should carry the weight of the reliability claim. Saying this out loud is stronger than
pretending the market metric is definitive.

---

## 5. Scope discipline

- **In scope (Capstone):** a single, fixed, well-justified orchestration policy + verification
  loop, evaluated against the baseline(s) on the tasks above.
- **Out / explicit future work:** *meta-learning / self-improving coordination.* The proposal
  currently claims the engine will "adaptively improve coordination over time" — that is hard to
  build *and* evaluate in the available window and risks overclaiming at a filter checkpoint. It
  is deferred to future work, stated plainly.

---

## 6. Primary-data plan (required for the final defence; designed/started before midterm)

The Capstone bar requires primary data analysis, and the midterm wants "real progress, not ideas."
Even though the build waits, the primary research should be **designed now and started**:

- **Interviews** — ~10 Lithuanian/EU SME export leads. Interview guide drafted before the midterm;
  first contacts initiated.
- **Survey** — concept appeal and willingness to pay.
- **Pilot (later phase)** — 3 SMEs test the recommendations on real or simulated scenarios.

These supply the perceived-usefulness and willingness-to-pay evidence and satisfy the
primary-data-analysis requirement that secondary data alone does not meet.

---

## 7. Timeline reconciliation

| Phase | Window | Deliverable |
|---|---|---|
| Design + evidence (midterm) | now – end June | Verified problem; orchestration core defined; RQ + evaluation design; preliminary lit review showing the gap; primary-research instruments drafted/started; preliminary expected MVP. **No software.** |
| Build + evaluate | July – Oct | Choose architecture; build the orchestration engine; run the evaluation vs baseline. |
| Pilot + analyse | Oct – Nov | SME pilots; primary-data analysis. |
| Report | Nov – Dec | Final report and defence. |

---

## 8. One-line framing for the midterm

> Our deep-tech contribution is an orchestration engine for SME export decisions, with a
> verification step for high-stakes compliance outputs. We will test whether it beats a single-LLM
> baseline on accuracy and reliability, using open trade data and a curated compliance test set.
> The internal architecture (multi-LLM vs multi-component) is a build-phase decision; the research
> question and the evaluation are fixed now.
