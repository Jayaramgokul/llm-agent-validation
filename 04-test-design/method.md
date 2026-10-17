# How the tests were derived

## Why a model checklist is not enough

A standard model validation asks about data, conceptual soundness, outcomes
and monitoring, for a model that takes numbers in and gives numbers out. A
language-model agent also talks to the client, adapts to what the client
says, gives different answers on different runs, is often graded by another
model, and rests on a model the firm does not control. Research has already
studied each of these behaviours and how to measure them, so the tests here
come from reading that research as a set of lenses.

## One source, one lens

Each source was read with the same question: *if this is right, what would
an existing validation miss?* Each answer became a candidate test.

| Lens | Main sources | Question |
|---|---|---|
| [Behaviour when the user changes](../03-research/behaviour-when-the-user-changes.md) | Perez et al. (2023); Sharma et al. (2024); Poole-Dayan et al. (2024) | Does the advice change when the user changes and the facts do not? |
| [Guardrails under attack](../03-research/guardrails-under-attack.md) | Perez et al. (2022); Ganguli et al. (2022); Clopper & Pearson | Can deliberate prompts break the rules, and what can the sample prove? |
| [Measuring honestly](../03-research/measuring-honestly.md) | Zheng et al. (2023); Wang et al. (2024); Miller (2024) | Is the judge fair, and is a change bigger than the noise? |
| [Honest confidence](../03-research/honest-confidence.md) | Kadavath et al. (2022); Guo et al. (2017) | When the agent sounds sure, is it right that often, for everyone? |
| [Consistency and change](../03-research/consistency-and-change.md) | Sclar et al. (2024); Saria & Subbaswamy (2019) | Same question, same answer? Does each update make anything worse? |
| [The agent in operation](../03-research/the-agent-in-operation.md) | Jacovi & Goldberg (2020); WEF Companion; Beyer et al. (1999) | Are explanations faithful, failures safe, and decisions rebuildable? |
| [Third-party models](../03-research/third-party-models.md) | NIST AI 600-1; Sharma et al. (2024); interagency guidance | What do we know about the rented model, and what was it tuned to reward? |

## What every test entry contains

- the principle from the source;
- the objective in plain language;
- the harm to the client;
- why existing tests miss it;
- the data needed;
- the method;
- pass criteria agreed *before* testing;
- how it relates to neighbouring tests.

## Three disciplines

1. **Paired designs and a noise floor.** A language model is never compared
   with itself on one run. Every comparison is paired (same profile, same
   question) and judged against measured run-to-run variation (M2).
2. **Decide the bar before looking.** Tolerances, personas, attack categories
   and phrase meanings are fixed in advance.
3. **Count the tests, and doubt the instrument.** Results across slices are
   corrected for multiple testing (M3), and any LLM judge is validated
   against people before its verdicts count (M1).

## From a test to an illustration

Where a test can be shown on simulated outcomes, there is a short standalone
script in [05-illustrations](../05-illustrations/). None of them calls a
language model. Each simulates what an evaluation would record and shows how
to analyse and read it.
