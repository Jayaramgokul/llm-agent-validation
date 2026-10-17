# Guardrails under attack

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from simulated outcomes in
> [05-illustrations](../05-illustrations/); no language model was called.

## Why this lens

An agent's rules (stay within the profile, never guarantee returns, disclose
fees, protect vulnerable clients, refuse to help with financial crime, keep
its instructions confidential) are only as strong as their weakest prompt.
Red-teaming, deliberately trying to make the system break its rules, is now
standard practice (Perez et al., 2022; Ganguli et al., 2022), and FINRA
Regulatory Notice 24-09 makes clear that existing supervisory obligations
apply to generative AI.

The weakness I see most often is not in the attacks but in the **reporting**.
A guardrail is declared robust because it passed a few dozen prompts, run
once each. That sample cannot support the claim. This lens is about designing
the red-team so that its result means something.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Perez et al. (2022), *Red Teaming Language Models with Language Models* | Attacks can be generated at scale and organised by category. | A structured battery: categories x scenarios x sophistication (G1) |
| Ganguli et al. (2022), *Red Teaming Language Models to Reduce Harms* | Human red-teaming finds diverse failures; results depend heavily on attacker skill and attack type. | Sophistication levels reported separately (G1) |
| Clopper & Pearson (1934); the "rule of three" | With zero failures in n trials, the 95% upper bound on the rate is about 3/n. | Report upper bounds and size the test to the target rate (G1) |
| Miller (2024), *Adding Error Bars to Evals* | Repeated samples of one question are clustered, not independent. | Intervals from resampling prompts, not replies (G1) |

## The tests

---

### G1. Red-team failure rate with honest intervals

**Principle.** A pass rate on a sample of prompts is an estimate. Repeated
runs of one prompt are not independent evidence. And zero failures does not
mean a zero failure rate.

**Objective.** Estimate how often the agent breaks its rules under attack,
with an interval that reflects both the sample of attacks and the model's
randomness, and say what the sample can prove.

**Client harm.** Guardrails are declared robust; in use, a few percent of
determined attempts succeed, against clients, against the firm's
obligations, or both.

**Why existing tests miss it.** Red-team results are usually reported as a
pass rate on one run per prompt, with no interval and no statement of power.

**Data.** A hand-written battery: 8 categories (risk override, guarantees,
discrimination, fees and conflicts, jailbreaks, vulnerable customers, privacy
and leakage, financial crime), 6 scenarios each, at 3 levels (basic,
social-engineering, jailbreak pattern), plus 36 legitimate control questions.
Each is run three times. Replies are graded first by code (for example, a
hidden canary string that must never appear), then by an LLM judge whose
verdict counts only if the sentence it quotes really appears in the reply
(see M1).

**Method.**
1. Failure rate overall, by category and by level.
2. Intervals by resampling prompts (a cluster bootstrap), not replies.
3. For categories with no failures, the exact upper bound.
4. The number of failure-free prompts needed to support each target rate.
5. Over-refusal on the control questions, reported beside the failure rate.

**Setting the pass criteria.** The upper bound of the interval, not the point
estimate, must be below the agreed rate, and over-refusal must stay below its
own limit. A guardrail that refuses everything is not a pass.

**What the illustration shows.** 432 replies give a failure rate of 4.2%.
Treating every reply as independent gives an interval of 2.7% to 6.5%;
resampling prompts gives the honest 1.4% to 7.2%. Advanced attacks fail most
often (6.9%). Financial crime has no failures in 18 prompts, yet its true
rate could be as high as 15%. Showing a rate below 5% needs 59 failure-free
prompts, and below 1% needs 299.
[`g1_red_team_failure_rate.py`](../05-illustrations/g1_red_team_failure_rate.py)

**Adjacent tests.** M1 (validating the judge), M3 (many slices).
**Regulatory hook.** FINRA Regulatory Notice 24-09; SEC IM Guidance 2017-02
(testing). **NIST AI RMF.** MEASURE 2.7.

---

### G2. Adversarial robustness: the smallest change that flips the outcome

**Principle.** An attack does not have to be a clever prompt. Small changes
to the structured inputs an agent collects can move a client across a
threshold.

**Objective.** Measure how many clients sit within one or two answer
changes of a different outcome, and whether consistency checks catch
implausible changes.

**Client harm.** A client, or an agent steered into "helping", unlocks a
product the client's real answers do not support.

**Why existing tests miss it.** Thresholds are validated on honest answers.

**Data.** Questionnaire answers and the eligibility rule.

**Method.**
1. For each ineligible client, find the fewest answer changes that would make
   them eligible.
2. Apply the firm's consistency checks to those altered answer sets.

**Setting the pass criteria.** The share of clients within easy reach of each
threshold is known and accepted, and the consistency checks catch an agreed
share of implausible changes.

**What the illustration shows.** 8.1% of all clients could unlock the
highest-risk band by changing one answer, and 18.2% by changing two. A
simple spread-based consistency check catches only 13% of the two-answer
cases, so it is not an adequate control on its own.
[`g2_smallest_flipping_change.py`](../05-illustrations/g2_smallest_flipping_change.py)

**Regulatory hook.** Compliance Rule 206(4)-7 (controls). **NIST AI RMF.** MEASURE 2.7.

## How the tests fit together

G1 tests the conversational surface; G2 tests the structured inputs behind
it. Both report what the evidence can and cannot prove.
