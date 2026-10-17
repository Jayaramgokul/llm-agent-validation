# Consistency and change

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from simulated outcomes in
> [05-illustrations](../05-illustrations/); no language model was called.

## Why this lens

A recommendation has to be defensible: to the client, to a complaints
handler, to an examiner. That needs two things a language model does not
give by default:

- **consistency**: the same client gets the same advice;
- **controlled change**: each update to the model, prompt or vendor is tested
  before it reaches clients.

Sclar et al. (2024) showed that meaning-preserving changes to prompt
formatting alone moved one open model's accuracy by up to 76 points. Model-risk
guidance ties validation to model changes; SR 26-2 leaves generative AI to
firms' own governance, so the firm has to decide that, for an agent, every
prompt edit and every vendor model update is a model change.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Sclar et al. (2024), *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design* | Performance should be reported across plausible prompt variants, not for one fixed format. | Reproducibility across runs and environments (V1); locked regression batteries (V2) |
| Miller (2024), *Adding Error Bars to Evals* | Compare versions on paired questions with honest error bars. | Old-against-new comparisons (V4) |
| Saria & Subbaswamy (2019), *Safe and Reliable Machine Learning* | Updates should be checked for safety, not only for average improvement. | Cell-by-cell regression checks (V4) |
| SR 26-2 (2026) | Validation timing should reflect the frequency and scope of model changes; generative AI is left to firms' own governance. | V2 to V4 |

## The tests

---

### V1. Determinism and reproducibility

**Principle.** If asking again could produce a different recommendation,
the recommendation cannot be defended as *the* advice.

**Objective.** Measure how often the same client receives different
recommendations across runs, and where that happens.

**Client harm.** Two identical clients, or the same client on two days,
receive different portfolios for no reason related to them.

**Why existing tests miss it.** Validation runs each test case once.

**Data.** A fixed panel of client profiles, each run many times, and across
environments (validation and production).

**Method.**
1. Run each profile repeatedly.
2. The share of profiles receiving more than one recommendation, and how
   dominant the most common one is.
3. Where the unstable profiles sit (here, near bucket boundaries).

**Setting the pass criteria.** Recommendations are identical across runs, or
vary only within a documented and disclosed band. Boundary cases get a
deterministic rule.

**What the illustration shows.** 30% of 50 profiles receive more than one
portfolio over ten runs. All of them are near a bucket boundary: 71% of
boundary profiles are unstable, against none elsewhere. The fix is targeted:
a deterministic rule at the boundaries.
[`v1_determinism.py`](../05-illustrations/v1_determinism.py)

**Regulatory hook.** Books and records (Advisers Act Rule 204-2); Compliance
Rule 206(4)-7. **NIST AI RMF.** MEASURE 2.5.

---

### V2. Cross-version behaviour regression

**Objective, method and pass criteria.** Keep a locked battery of the
behaviour tests (B1 to B3, G1) and run it on every new model, prompt or
vendor version, comparing with the previous version using the noise floor
(M2) and paired comparisons. Pass if no behaviour worsens beyond tolerance.
**Client harm.** An update quietly makes the agent more sycophantic or
easier to jailbreak.
**Regulatory hook.** Model-risk principles by extension (change control); FINRA Regulatory Notice
24-09. **NIST AI RMF.** MEASURE 2.4.

### V3. Validation equals production

**Objective, method and pass criteria.** Compare the validation and
production environments: model snapshot identifiers, prompt versions,
retrieval indexes, library versions and data schemas. Pass if there are no
material differences, or re-validation is triggered.
**Client harm.** Clients are served by a configuration nobody validated.
**Regulatory hook.** Model-risk principles by extension (change control). **NIST AI RMF.** MEASURE 2.4.

---

### V4. Safe model updates

**Principle.** A version that is better on average can be worse for a
group or a situation (Saria & Subbaswamy, 2019).

**Objective.** Compare old and new versions cell by cell (persona by
category), correcting for the number of cells, before release.

**Client harm.** An update ships because it improves the average, and makes
the agent worse for a particular group of clients in a situation that
matters.

**Why existing tests miss it.** Release decisions are taken on aggregate
metrics.

**Data.** Results for both versions on the same battery, by cell.

**Method.**
1. Failure rate per cell for each version.
2. A one-sided test per cell for "new is worse".
3. Benjamini-Hochberg across cells.

**Setting the pass criteria.** No cell regresses beyond tolerance after
correction without a documented mitigation.

**What the illustration shows.** The new version lowers the overall failure
rate from 6.7% to 5.5%. For non-native speakers in vulnerable-customer
scenarios it rises from 7.5% to 16.8% (corrected q = 0.001).
[`v4_safe_updates.py`](../05-illustrations/v4_safe_updates.py)

**Regulatory hook.** Model-risk principles by extension (change control). **NIST AI RMF.** MEASURE 2.4.

## How the tests fit together

V1 makes each answer defensible; V2 to V4 keep it defensible through change.
All of them rest on the noise floor (M2) and the correction for many slices
(M3).
