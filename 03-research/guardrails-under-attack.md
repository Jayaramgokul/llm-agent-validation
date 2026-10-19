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

**Data.** A hand-written battery of attacks, organised so that results can
be read by category and by skill:
- **8 categories:** risk override, guarantees, discrimination, fees and
  conflicts, jailbreaks, vulnerable customers, privacy and leakage, and
  financial crime;
- **6 scenarios in each,** at **3 levels of sophistication:** a basic
  request, a social-engineering attempt, and a known jailbreak pattern;
- **36 legitimate control questions** that look similar but should be
  answered, to measure over-refusal;
- **three runs of every prompt,** since the agent's answer varies.

Replies are graded first by code where possible (for example, a hidden
"canary" string in the instructions that must never appear in a reply), then
by an LLM judge whose verdict counts only if the sentence it quotes really
appears in the reply (M1).

**Method.**
1. **Failure rate** overall, by category and by level.
2. **Intervals by resampling prompts** (a cluster bootstrap), not replies.
   Three runs of one prompt are not three independent tests: if a prompt
   works, it tends to work every time.
3. **For categories with no failures, the exact upper bound** on the rate
   (Clopper–Pearson, one-sided 95%). With zero failures in n prompts, it is
   about 3 ÷ n.
4. **The number of failure-free prompts needed** to support each target
   rate, so the battery can be sized in advance.
5. **Over-refusal on the control questions,** reported beside the failure
   rate. A guardrail that refuses legitimate questions also fails clients.

**Setting the pass criteria.** Agree, for each category, the highest failure
rate the firm will accept, and the highest over-refusal rate. Then:
- **Pass:** the upper end of the interval, not the point estimate, is below
  the agreed rate, and over-refusal is below its limit.
- **Inconclusive:** the battery is too small for the upper end to get there,
  even with no failures. The answer is a larger battery, not a pass.
- **Fail:** the interval sits above the agreed rate. A guardrail that
  refuses everything is not a pass either.

**What the illustration shows.** The script simulates the battery above:
144 attack prompts, each run three times. Most prompts never work, and the
few that do tend to work on most runs, as real jailbreaks do.

| Measure | Result |
|---|---|
| Overall failure rate | 4.2% of 432 replies |
| Interval treating every reply as independent | 2.7% to 6.5% |
| Interval resampling prompts (the right one) | 1.4% to 7.2% |
| Basic / intermediate / advanced attacks | 2.1% / 3.5% / **6.9%** (1.4–14.6%) |
| Financial crime | 0 failures in 18 prompts, but the rate could be up to **15%** |
| Failure-free prompts needed to show a rate below 5% / below 1% | 59 / 299 |
| Over-refusal on legitimate questions | 6% |

Treating each reply as independent makes the result look about twice as
precise as it is. The more skilled the attack, the more often it works.
Financial crime looks perfect, with no failures, but 18 prompts can only show
that its rate is below 15%. Claiming it is below 5% would need 59
failure-free prompts, and below 1% would need 299. Most published red-team
results could not support the claims made from them.

![Red-team failure rates with intervals, overall and by attack level](../05-illustrations/output/g1_failure_rates.png)

*The grey interval treats every reply as independent and looks precise; the
blue one below it, from resampling prompts, is the honest width. Financial
crime has no failures, but its interval still reaches 15%.*

[`g1_red_team_failure_rate.py`](../05-illustrations/g1_red_team_failure_rate.py)

**Adjacent tests.**
- **M1** validates the judge that grades the replies; a judge that misses
  failures makes this test look better than it is.
- **M3** controls false alarms across the many category-by-level slices.
- **B2** uses the same exact bounds for claims of professional status.

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

**Data.**
- **The structured inputs the agent collects,** such as the answers to a
  risk questionnaire, for a representative set of clients.
- **Every eligibility rule** that turns those inputs into access to a
  product or band.
- **The firm's consistency checks,** the rules meant to catch answers that do
  not fit together.

**Method.**
1. **For each client who is not eligible,** find the fewest answer changes
   that would make them eligible. On a scored questionnaire, the cheapest
   route is to raise the lowest answers to the maximum.
2. **Report the share of all clients within one, and within two, changes**
   of each threshold.
3. **Apply the firm's consistency checks** to those altered answer sets, and
   measure the share that the checks would flag.
4. **Ask how the agent behaves** when a client asks which answer would change
   the result, or asks to revise an answer just after being refused. An
   agent that coaches clients across thresholds turns this weakness into a
   live risk.

**Setting the pass criteria.** The share of clients within easy reach of
each threshold is known and accepted by the model owner, and the consistency
checks catch an agreed share of implausible changes. Where they do not,
stronger controls are needed, such as follow-up questions when an answer
changes, or a human review before access to the riskiest products.

**What the illustration shows.** The script simulates 5,000 clients
answering an eight-question questionnaire. A score of 75 out of 100 unlocks
the highest-risk band, and 82% of clients fall short of it.

| Measure | Share of all clients |
|---|---|
| Could become eligible by changing one answer | 8.1% |
| Could become eligible by changing at most two answers | 18.2% |

A simple consistency check, which flags answer sets that are unusually
spread out, catches only 13% of the two-answer cases. Nearly one client in
five could reach the riskiest band by changing two answers, and the check
would let almost all of them through. It is not an adequate control on its
own.
[`g2_smallest_flipping_change.py`](../05-illustrations/g2_smallest_flipping_change.py)

**Adjacent tests.**
- **B2** tests a conversational lever on the same limits: claims of
  professional status.
- **O2** checks what happens when inputs arrive broken rather than
  manipulated.

**Regulatory hook.** Compliance Rule 206(4)-7 (controls). **NIST AI RMF.** MEASURE 2.7.

## How the tests fit together

G1 tests the conversational surface; G2 tests the structured inputs behind
it. Both report what the evidence can and cannot prove.
