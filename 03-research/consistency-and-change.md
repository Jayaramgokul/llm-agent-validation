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

**Data.**
- **A fixed panel of client profiles,** covering every risk band, with
  deliberately more profiles close to the boundaries between bands, where
  instability is most likely.
- **Many runs of each profile** (ten here), with the agent's settings
  recorded: model snapshot, temperature, prompt version.
- **The same panel run in each environment,** validation and production, to
  check that they agree.

**Method.**
1. **Run each profile repeatedly** with identical inputs.
2. **Measure instability:** the share of profiles that receive more than one
   recommendation, and, for each, how often the most common one appears.
3. **Find where the unstable profiles sit,** for example near band
   boundaries, or in particular kinds of request.
4. **Repeat across environments.** A profile that is stable in validation
   but gets a different answer in production points to a configuration
   difference (V3).

**Setting the pass criteria.** Recommendations are identical across runs, or
vary only within a documented and disclosed band. Profiles that cannot be
made stable, typically those on a boundary, get a deterministic rule outside
the language model, so the same inputs always give the same advice and the
record can be reproduced.

**What the illustration shows.** The script simulates 50 client profiles at
different points on the risk scale, each run ten times. Profiles close to a
boundary between bands have a real chance of landing in the neighbouring
band on any run.

| Measure | Result |
|---|---|
| Profiles that always get the same portfolio | 70% |
| Profiles that get more than one portfolio | 30% |
| Instability among profiles near a band boundary | 71% |
| Instability elsewhere | 0% |

Three profiles in ten could have received a different portfolio just by
asking again, so a complaint about any of them would be hard to defend. The
instability is not spread evenly, though: it sits entirely with profiles
near a boundary. That makes the fix targeted: a deterministic rule for
boundary cases, rather than a wholesale change to the agent.
[`v1_determinism.py`](../05-illustrations/v1_determinism.py)

**Adjacent tests.**
- **M2** measures the same randomness for evaluation scores.
- **O3** needs reproducibility to rebuild any past decision.
- **V3** checks that the environments being compared really are the same.

**Regulatory hook.** Books and records (Advisers Act Rule 204-2); Compliance
Rule 206(4)-7. **NIST AI RMF.** MEASURE 2.5.

---

### V2. Cross-version behaviour regression

**Objective.** Run a fixed battery of behaviour tests on every new version
of the model, prompt or vendor model, and stop any version that makes
behaviour worse.

**Client harm.** An update quietly makes the agent more sycophantic or
easier to jailbreak.

**Why existing tests miss it.** Updates are usually checked for task
performance. Behaviours such as sycophancy or resistance to jailbreaks are
tested once, at launch, and not again.

**Data.** A locked battery of the behaviour tests (B1 to B3 and G1, plus the
capability questions from B4), kept unchanged between versions, and results
for the previous version on the same battery.

**Method.**
1. **Lock the battery:** the same prompts, profiles and grading for every
   version, stored with a version number. Adding new tests is fine; changing
   existing ones breaks the comparison.
2. **Run every new version** on the full battery, with several runs per
   prompt.
3. **Compare with the previous version** using the noise floor (M2) and
   paired comparisons by prompt, slice by slice.
4. **Correct for the number of slices** (M3) before reporting any regression.

**Setting the pass criteria.** Pass if no behaviour worsens beyond the
agreed tolerance after correction. A regression blocks the release unless
there is a documented mitigation and sign-off.

**Adjacent tests.**
- **V4** applies the same idea cell by cell, for groups of clients.
- **M2** and **M3** provide the comparison method.

**Regulatory hook.** Model-risk principles by extension (change control); FINRA Regulatory Notice
24-09. **NIST AI RMF.** MEASURE 2.4.

### V3. Validation equals production

**Objective.** Confirm that the configuration serving clients is the one
that was validated.

**Client harm.** Clients are served by a configuration nobody validated.

**Why existing tests miss it.** Validation happens in one environment and
production runs in another. Small differences, such as a newer model
snapshot or an edited prompt, are easy to miss.

**Data.** For each environment: the model snapshot identifier, the prompt
version, the retrieval index and its contents date, the library versions,
the data schemas and any configuration settings.

**Method.**
1. **Record the full configuration** of the validated environment at sign-off.
2. **Compare it, item by item,** with production, at release and on a regular
   schedule afterwards.
3. **Run the V1 panel in both environments** as a functional check, since two
   configurations can look identical on paper and behave differently.

**Setting the pass criteria.** Pass if there are no material differences.
Any material difference triggers re-validation of the affected parts before
clients are served.

**Adjacent tests.**
- **V1** gives the functional check.
- **T2** covers the vendor's side: whether the firm is told when the
  underlying model changes.

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

**Data.** Results for both versions on the same battery, broken down into
cells: each combination of client persona and test category, with enough
replies in every cell to compare.

**Method.**
1. **Failure rate per cell** for each version.
2. **A one-sided test per cell** for "the new version is worse", since an
   improvement in a cell is not a concern.
3. **Benjamini–Hochberg across cells,** because with many cells some will
   look worse by chance.
4. **Look at the regressions that survive,** and at what the cell has in
   common with the change that was made.

**Setting the pass criteria.** Agree the tolerance and the false discovery
rate before release. Pass if no cell regresses beyond tolerance after
correction, or each regression has a documented mitigation, such as routing
that cell's cases to a human until it is fixed.

**What the illustration shows.** The script simulates 24 cells (six personas
by four test categories), with 400 replies per cell for each version. The
update cuts the failure rate by about 30% in every cell but one, where it
breaks something.

| Measure | Old version | New version |
|---|---|---|
| Overall failure rate | 6.7% | 5.5% |
| Non-native speakers in vulnerable-customer scenarios | 7.5% | **16.8%** (corrected q = 0.001) |

On the average, the update is a clear improvement and would be released. In
one cell, the failure rate more than doubles, and that cell is non-native
speakers in situations where the client is vulnerable: the group a firm most
needs to protect. The cell-by-cell comparison, with the correction, finds it
and nothing else.
[`v4_safe_updates.py`](../05-illustrations/v4_safe_updates.py)

**Adjacent tests.**
- **V2** runs the full behaviour battery on every version; V4 makes the
  release decision by cell.
- **K2** and **B3** look at other ways the agent can serve some clients
  worse than others.

**Regulatory hook.** Model-risk principles by extension (change control). **NIST AI RMF.** MEASURE 2.4.

## How the tests fit together

V1 makes each answer defensible; V2 to V4 keep it defensible through change.
All of them rest on the noise floor (M2) and the correction for many slices
(M3).
