# Measuring a language model honestly

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from simulated outcomes in
> [05-illustrations](../05-illustrations/); no language model was called.

## Why this lens

Every other test in this repository produces a number from an evaluation:
failure rates, accuracy, calibration. Language-model evaluations have three
features that make those numbers easy to misread:

- the grader is often another language model;
- the same model gives different answers on different runs;
- results are sliced many ways.

Model-risk guidance asks for effective challenge of models. SR 26-2 leaves
generative AI to firms' own governance, but the principle carries over, and
here it has to include challenging the measurement itself.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Zheng et al. (2023), *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* | Strong LLM judges can agree with humans about as well as humans agree with each other, but show position, verbosity and self-preference biases. | Validate the judge against humans and test its biases (M1) |
| Wang et al. (2024), *Large Language Models are not Fair Evaluators* | Simply swapping the order of two answers can reverse the judge's verdict. | An order-swap test (M1) |
| Miller (2024), *Adding Error Bars to Evals* | Treat an evaluation as an experiment: clustered standard errors, several samples per question, paired differences between models, and power analysis. | Noise floor first, then paired comparisons (M2) |
| Benjamini & Hochberg (1995) | Control the false discovery rate across many comparisons. | Correction across slices (M3) |

## The tests

---

### M1. Validating the judge

**Principle.** An LLM judge is a model, with its own error rate and biases
(Zheng et al., 2023; Wang et al., 2024).

**Objective.** Before any judged result is used, measure the judge's
agreement with human reviewers, how many real failures it misses, and
whether answer order or length sways it.

**Client harm.** A judge that misses failures makes the agent look safer than
it is. A judge that prefers longer answers rewards padding over accuracy.

**Why existing tests miss it.** The judge is treated as a measuring
instrument, not as a model under validation.

**Data.** A sample of replies labelled independently by human reviewers;
pairs of answers shown in both orders; answers of similar quality and
varying length.

**Method.**
1. Cohen's kappa between judge and humans, with a bootstrap interval.
2. The share of human-identified failures the judge catches.
3. Present each pair in both orders and check that the verdict holds.
4. Regress the judge's score on length, holding human-rated quality fixed.
5. Require the judge to quote the evidence for each verdict, and check by code
   that the quote really appears in the reply.

**Setting the pass criteria.** Minimum kappa and catch rate; a maximum share
of order reversals; a length effect within tolerance. Where the catch rate is
below 100%, reported failure rates are corrected or a human sample is
reviewed.

**What the illustration shows.** Agreement is good (kappa 0.79), but the
judge catches 41 of 46 real failures (89%), so its failure rates understate
the truth. With the order swapped, its choice holds in only 56% of pairs. It
picks answer A 66% of the time when A is shown first and 41% when shown
second. Holding quality fixed, each extra 100 words adds about a third of a
point.
[`m1_validating_the_judge.py`](../05-illustrations/m1_validating_the_judge.py)

**Regulatory hook.** Model-risk principles by extension (effective challenge); FINRA Regulatory Notice
24-09. **NIST AI RMF.** MEASURE 2.13.

---

### M2. Know the noise first

**Principle.** An unchanged model does not score the same twice. Several
samples per question and paired comparisons reduce the noise (Miller, 2024).

**Objective.** Measure the run-to-run variation of the current version
before comparing any new version against it.

**Client harm.** A prompt change is shipped because one lucky run looked
better, or a good change is rolled back because of one unlucky run.

**Why existing tests miss it.** Versions are compared on one run each, as if
the scores were fixed.

**Data.** The evaluation set; the current and candidate versions.

**Method.**
1. Run the current version several times unchanged; take the 95th
   percentile of differences between runs as the noise floor.
2. Compare versions on several runs each, paired by question, with a
   bootstrap interval.

**Setting the pass criteria.** A change is reported as real only if its
interval excludes zero, and it is treated as material only beyond the agreed
size.

**What the illustration shows.** Ten unchanged runs score between 68% and
77%; the noise floor is 7.8 points. One run each shows the new version 3.7
points *worse*, well inside the noise floor. Five runs each, paired by
question, give +2.1 points (95% CI −0.7 to +5.0): not distinguishable from
noise.
[`m2_noise_floor.py`](../05-illustrations/m2_noise_floor.py)

**Regulatory hook.** Model-risk principles by extension (change control). **NIST AI RMF.** MEASURE 2.13.

---

### M3. Multiple testing across the suite

**Principle.** Slicing results by category, level and persona multiplies the
number of tests, and with it the chance alarms.

**Objective.** Report regressions across slices with the false discovery
rate controlled.

**Client harm.** Real regressions are lost among false alarms, or releases
are blocked by noise until the alarms are ignored.

**Method.** Collect the p-value of every slice comparison and apply
Benjamini-Hochberg at the agreed rate. Keep uncorrected results as
exploratory.

**What the illustration shows.** Across 144 slices with 3 genuine
regressions, reading each at p < 0.05 raises 6 alarms, 3 of them false. With
the false discovery rate controlled at 10%, the 3 real regressions remain and
the false ones go.
[`m3_multiple_testing.py`](../05-illustrations/m3_multiple_testing.py)

**Regulatory hook.** Model-risk principles by extension (effective challenge). **NIST AI RMF.** MEASURE 2.13.

## How the tests fit together

M1 checks the instrument, M2 the noise, M3 the number of looks. Every other
lens relies on all three.
