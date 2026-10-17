# The agent in operation

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from simulated outcomes in
> [05-illustrations](../05-illustrations/); no language model was called.

## Why this lens

Once live, an agent has to do four things a model test rarely checks:

- explain itself truthfully;
- fail safely when a dependency breaks;
- leave a record from which any decision can be rebuilt;
- if it retrieves "similar" cases, retrieve ones that really are similar.

The *Companion to the Model AI Governance Framework* (WEF, IMDA and PDPC,
2020) frames these as operational questions across the life cycle. FINRA
rules on books and records, complaints and business continuity make them
obligations.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Jacovi & Goldberg (2020), *Towards Faithfully Interpretable NLP Systems* | Plausibility (does an explanation sound right?) and faithfulness (does it reflect the model's reasoning?) are different, and faithfulness must be tested. | A deletion test for stated reasons (O1) |
| WEF, IMDA & PDPC (2020), *Companion to the Model AI Governance Framework* | Plan for failure, keep records, and explain decisions to the people affected. | Failing safely (O2); rebuilding any decision (O3) |
| Beyer et al. (1999), *When Is "Nearest Neighbor" Meaningful?* | In high dimensions, without structure, the nearest and farthest points become almost equally far away. | Checking that retrieval finds meaningful neighbours (O4) |

## The tests

---

### O1. Explanations that are faithful

**Principle.** An explanation can be plausible without being faithful
(Jacovi & Goldberg, 2020). Faithfulness can be tested: if the stated reasons
really drove the outcome, removing them should change it more than removing
other factors.

**Objective.** Check that the reasons the agent gives for each
recommendation are the factors that actually drive it.

**Client harm.** Clients, and complaint handlers, are given reasons that
sound right but are not why the advice was given.

**Why existing tests miss it.** Explanations are reviewed for clarity and
tone, not tested against the model's behaviour.

**Data.** The scoring model, client inputs, and the reasons stated for each
recommendation.

**Method.**
1. For each client, neutralise the stated reasons and measure the change in
   the score.
2. Do the same with randomly chosen factors.
3. Compare.

**Setting the pass criteria.** Stated reasons must move the outcome by
clearly more than random factors, by an agreed margin.

**What the illustration shows.** Generic template reasons ("time horizon,
risk tolerance, experience") change the score no more than random factors
(1.0 times). Reasons taken from actual contributions change it 1.4 times as
much.
[`o1_faithful_explanations.py`](../05-illustrations/o1_faithful_explanations.py)

**Regulatory hook.** Disclosure of how the algorithm works (SEC IM Guidance
2017-02). **NIST AI RMF.** MEASURE 2.9.

---

### O2. Failing safely

**Objective, method and pass criteria.** Inject each dependency failure
(model API down, timeout, malformed output, retrieval unavailable, market
data stale) and check the agent's behaviour, logging and message to the
client. Pass if every failure produces the specified safe behaviour, for
example a clear message and handover, never a confident answer built on
missing data.
**Client harm.** The agent fails silently or answers confidently without the
information it needs.
**Regulatory hook.** FINRA Rule 4370 (business continuity). **NIST AI RMF.** MANAGE 2.3.

### O3. Rebuilding any past decision

**Objective, method and pass criteria.** Sample past recommendations and
rebuild each from the logs: inputs, conversation, model snapshot, prompt
version, retrieved context, output. Pass if sampled decisions are fully
reconstructible at the agreed rate.
**Client harm.** A complaint cannot be investigated because nobody can say
why the advice was given.
**Regulatory hook.** Books and records (Rule 204-2); FINRA Rules 4511 and
4513. **NIST AI RMF.** MEASURE 2.8.

---

### O4. Similarity in high dimensions

**Principle.** As dimensions grow, distances between unstructured points
concentrate, so the "nearest" neighbour is barely nearer than the farthest
(Beyer et al., 1999).

**Objective.** For each component that retrieves "similar" clients or
questions, show that its neighbours are meaningfully closer than other items.

**Client harm.** Advice is shaped by "clients like you" who are not like the
client at all.

**Why existing tests miss it.** Retrieval is judged by whether results look
relevant on a few examples.

**Method.** Compare nearest-neighbour distances with those to random or
distant items (relative contrast) on the production embedding space, and
against an unstructured baseline of the same dimension.

**Setting the pass criteria.** Relative contrast clearly above the
unstructured baseline, by an agreed margin.

**What the illustration shows.** With no structure, relative contrast falls
from 4.7 in 8 dimensions to 0.16 in 768. With 30 real client types in 768
dimensions it recovers to 1.03.
[`o4_similarity_high_dimensions.py`](../05-illustrations/o4_similarity_high_dimensions.py)

**Regulatory hook.** Duty of care. **NIST AI RMF.** MEASURE 2.5.

## How the tests fit together

O1 checks what the agent says about its decisions; O3 checks what the firm
can say afterwards. O2 covers the moments when things break, and O4 the
retrieval components that quietly shape answers.
