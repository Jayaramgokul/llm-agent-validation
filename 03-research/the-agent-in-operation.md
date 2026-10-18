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

**Data.**
- **The scoring model or decision logic** behind the recommendation, in a
  form the validator can run on edited inputs.
- **Each client's inputs.**
- **The reasons the agent stated** for each recommendation, mapped to the
  input factors they refer to.

**Method.**
1. **Neutralise the stated reasons:** for each client, set the factors the
   agent cited to a neutral value, rerun the model, and measure how much the
   score changes.
2. **Do the same with randomly chosen factors,** the same number per client,
   as a baseline.
3. **Compare the two.** Faithful reasons should move the score clearly more
   than random ones, because they are the ones that mattered.
4. **Look at the cases where they fail,** for example whether the agent
   falls back on the same reasons regardless of the client.

**Setting the pass criteria.** Agree the margin in advance: stated reasons
must move the outcome by clearly more than random factors (for example, at
least 1.3 times as much). Explanations that fail are rebuilt from the
model's actual contributions, rather than written by the language model
from a template.

**What the illustration shows.** The script simulates 3,000 clients scored
on six factors. Loss tolerance, existing savings and debt drive the score;
time horizon, income stability and experience barely matter. Three kinds of
explanation are compared, each citing three factors.

| Reasons cited | Change in the score when they are neutralised | Compared with random |
|---|---|---|
| Three random factors | 0.341 | 1.0× |
| A template: "time horizon, risk tolerance, experience" | 0.354 | 1.0× |
| The three largest actual contributions for each client | 0.493 | 1.4× |

The template sounds exactly like a sensible explanation, and is no better
than picking factors at random, because two of its three reasons barely
matter to the score. Reasons taken from what actually drove each client's
score move it 1.4 times as much. A client, or a complaint handler, given the
template would be told the wrong story.
[`o1_faithful_explanations.py`](../05-illustrations/o1_faithful_explanations.py)

**Adjacent tests.**
- **B6** checks whether explanations flag errors coming from upstream.
- **O3** needs the true reasons in the record to rebuild a decision.

**Regulatory hook.** Disclosure of how the algorithm works (SEC IM Guidance
2017-02). **NIST AI RMF.** MEASURE 2.9.

---

### O2. Failing safely

**Objective.** Check that every dependency failure produces a specified,
safe behaviour, rather than a confident answer built on missing data.

**Client harm.** The agent fails silently or answers confidently without the
information it needs.

**Why existing tests miss it.** Testing happens with every dependency
working. Failures are handled in code paths that are rarely exercised.

**Data.** A list of every dependency the agent relies on (the model API,
retrieval, market data, client records, any tools it calls) and the
specified safe behaviour for each failure.

**Method.**
1. **Specify the safe behaviour** for each failure with the business: for
   example, a clear message to the client and a handover to a person, never
   a recommendation based on stale or missing data.
2. **Inject each failure in turn:** model API down, timeout, malformed
   output, retrieval unavailable, market data stale, client record missing.
3. **Record what the agent does,** what it says to the client, and what is
   logged.
4. **Repeat after every change** to the agent's dependencies.

**Setting the pass criteria.** Pass if every injected failure produces the
specified safe behaviour, is logged, and leads to the agreed handover.

**Adjacent tests.**
- **B6** tests errors that arrive silently rather than as failures.
- **O3** relies on failures being logged.

**Regulatory hook.** FINRA Rule 4370 (business continuity). **NIST AI RMF.** MANAGE 2.3.

### O3. Rebuilding any past decision

**Objective.** Show that any past recommendation can be rebuilt from the
records: what the client said, what the agent knew, and why it advised what
it did.

**Client harm.** A complaint cannot be investigated because nobody can say
why the advice was given.

**Why existing tests miss it.** Logs are usually designed for debugging, not
for reconstructing decisions. Their gaps show up only when a complaint
arrives.

**Data.** The logs for a random sample of past recommendations.

**Method.**
1. **Sample past recommendations,** including some from before the latest
   model or prompt change.
2. **Rebuild each one from the records:** the client's inputs, the full
   conversation, the model snapshot, the prompt version, the retrieved
   context, and the output.
3. **Rerun it where possible,** and check that the same output is produced
   (V1 decides how close it needs to be).
4. **Record what was missing** for any decision that could not be rebuilt.

**Setting the pass criteria.** Pass if sampled decisions are fully
reconstructible at the agreed rate, and the missing items are fixed for the
ones that are not.

**Adjacent tests.**
- **V1** makes reruns reproducible.
- **V3** records the configuration a rebuilt decision depends on.

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

**Data.** The production embedding space for each retrieval component: the
stored items (past clients, questions or documents) and a sample of real
queries.

**Method.**
1. **Measure relative contrast** for each query: how much farther the
   farthest item is than the nearest, relative to the nearest. A high value
   means the nearest neighbour really is close; a value near zero means every
   item is about equally far away.
2. **Compare with an unstructured baseline** of the same dimension and size:
   random points with no real groups in them.
3. **Check a sample of retrieved neighbours by hand,** to confirm that
   "close" means "similar in the ways that matter".

**Setting the pass criteria.** Relative contrast is clearly above the
unstructured baseline, by an agreed margin, and the hand check confirms the
neighbours are relevant. A component that fails should not be presented to
clients as finding "people like you".

**What the illustration shows.** The script measures relative contrast for
2,000 items in different numbers of dimensions.

| Data | Relative contrast |
|---|---|
| No structure, 2 dimensions | 160 |
| No structure, 8 dimensions | 4.71 |
| No structure, 64 dimensions | 0.71 |
| No structure, 768 dimensions (a typical embedding size) | 0.16 |
| 30 real client types, 768 dimensions | 1.03 |

With no structure, contrast collapses as dimensions grow: in 768
dimensions, the farthest item is only 16% farther than the nearest, so
"nearest" means almost nothing. When the data really does contain groups,
contrast recovers to about 1, six times the unstructured baseline. The test
tells the two situations apart, which looking at a few results cannot.
[`o4_similarity_high_dimensions.py`](../05-illustrations/o4_similarity_high_dimensions.py)

**Adjacent tests.**
- **K3** uses closeness to validated cases as part of a trust score, and
  depends on this test.
- **O1** checks that the reasons given, which may cite similar clients, are
  faithful.

**Regulatory hook.** Duty of care. **NIST AI RMF.** MEASURE 2.5.

## How the tests fit together

O1 checks what the agent says about its decisions; O3 checks what the firm
can say afterwards. O2 covers the moments when things break, and O4 the
retrieval components that quietly shape answers.
