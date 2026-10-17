# Organising the validation with the NIST AI RMF and the Generative AI Profile

> Descriptions are paraphrased from NIST AI 100-1 (2023) and NIST AI 600-1
> (2024); see [SOURCES.md](../SOURCES.md).

## Why use them

The NIST AI Risk Management Framework gives four functions for managing AI
risk:

- **GOVERN:** policies, accountability and culture;
- **MAP:** context, intended use and the risks that follow;
- **MEASURE:** analysing and tracking those risks;
- **MANAGE:** acting on what is found.

Its companion, NIST AI 600-1, the Generative AI Profile, lists twelve risks
that are new or made worse by generative AI. Together they gave a structure
for a validation that regulators, the business and the model owner could
all follow.

## How each function shaped this work

**GOVERN.**
- Tolerances, personas, attack categories and the meaning of each confidence
  phrase are agreed before testing.
- The judge is validated before its verdicts count (M1).
- Vendor models are governed through disclosure and spot-checks (T1, T2,
  under GOVERN 6.1).

**MAP.**
- The [regulatory map](../01-regulation/regulatory-map.md) sets out how an
  agent changes each existing obligation.
- The [governance gaps](../01-regulation/gaps-and-enforcement.md) set out
  where a standard validation has no evidence.
- The agent is mapped as a stack (vendor model, prompts, retrieval,
  guardrails, judge), because each layer can change separately.

**MEASURE.** Every test carries the subcategory it evidences:

| Subcategory | What NIST asks for (paraphrased) | Tests |
|---|---|---|
| MEASURE 2.4 | Behaviour is monitored in production | V2, V3, V4 |
| MEASURE 2.5 | Valid and reliable; limits of generalisation documented | B5, K3, V1, O4 |
| MEASURE 2.6 | Safety risks evaluated; residual risk within tolerance | B1, B6 |
| MEASURE 2.7 | Security and resilience evaluated | B2, G1, G2 |
| MEASURE 2.8 | Transparency and accountability risks examined | B4, O3 |
| MEASURE 2.9 | Outputs explained and interpreted in context | K1, O1 |
| MEASURE 2.11 | Fairness and bias evaluated | B3, K2 |
| MEASURE 2.13 | The measurement methods themselves are evaluated | M1, M2, M3 |
| MEASURE 3.1 | Emerging risks tracked in deployment | K4 |
| GOVERN 6.1 | Policies address third-party AI risks | T1, T2 |
| MANAGE 2.3 | Procedures to respond to and recover from failures | O2 |

**MANAGE.**
- Failures become findings with an owner and a re-test date.
- Safe failure (O2) and regression gates on every update (V2, V4) are
  management controls in their own right.

## The Generative AI Profile's risks, and where they are tested

| NIST AI 600-1 risk | What it means for a client-facing agent | Tests |
|---|---|---|
| Confabulation | Confident statements that are false | K1, B5, O1 |
| Harmful bias and homogenisation | Answer quality or confidence varying by how the client writes or who they seem to be | B3, K2 |
| Human-AI configuration | Over-reliance on fluent answers; false claims about capabilities | B4, B6, K1 |
| Information integrity | Misleading statements reaching clients at scale | B4, O1 |
| Information security | Prompt injection, jailbreaks, instruction leakage | G1, G2 |
| Data privacy | Client data leaking through the agent | G1 (privacy and leakage) |
| Dangerous, violent or hateful content | Help with fraud or other financial crime | G1 (financial crime) |
| Value chain and component integration | Vendor model changes and undisclosed tuning | T1, T2, V2, V3 |

The remaining profile risks (CBRN information; obscene, degrading or abusive
content; environmental impacts; intellectual property) are less specific to
client-facing financial services and are not tested here.
