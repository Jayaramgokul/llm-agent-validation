# What the rules require of LLM agents in regulated financial services

> Public sources only; see [SOURCES.md](../SOURCES.md). Rules are summarised,
> not quoted; check their current status before relying on them.

## The starting point: the rules do not change for AI

Regulators have been consistent that existing obligations apply whatever
technology delivers the advice. FINRA Regulatory Notice 24-09 says this
directly for generative AI: supervision, communications, recordkeeping and
vendor management rules apply as they always have. The validation question is
therefore not "which AI rules apply?" but **"how does a language-model agent
change the way each existing obligation can fail?"**

## A gap in model-risk guidance

SR 26-2, the model risk guidance that replaced SR 11-7 in April 2026, places
generative and agentic AI **outside its scope** and leaves their governance to
each firm's own risk management. Its principles still give the template:
effective challenge, outcomes analysis, ongoing monitoring and validation of
vendor models. In this repository, "model-risk principles by extension" means
applying those principles to a language-model agent as a matter of firm
policy, with the NIST AI RMF supplying the structure.

## Obligations and how an agent changes them

| Obligation | Source | How an LLM agent changes the risk | Tests |
|---|---|---|---|
| **Duty of care:** advice based on the client's actual objectives and circumstances | SEC Release IA-5248 (2019) | The agent can be swayed by what the client says, not just who the client is | [B1, B2, B3](../03-research/behaviour-when-the-user-changes.md) |
| **Fair and balanced communications;** no misleading claims | FINRA Rule 2210; SEC Marketing Rule 206(4)-1 | Every reply is a communication; confidence words and capability claims can mislead at scale | [K1](../03-research/honest-confidence.md), [B4](../03-research/behaviour-when-the-user-changes.md) |
| **Disclosure of how the algorithm works;** testing before and after launch | SEC IM Guidance Update 2017-02 | Explanations can be fluent but unfaithful; behaviour varies run to run | [O1](../03-research/the-agent-in-operation.md), [V1](../03-research/consistency-and-change.md) |
| **Supervision and controls** | FINRA Rule 3110; Advisers Act Compliance Rule 206(4)-7 | Controls must cover prompts, guardrails and the model itself | [G1, G2](../03-research/guardrails-under-attack.md), [B6](../03-research/behaviour-when-the-user-changes.md) |
| **Books and records** | Advisers Act Rule 204-2; FINRA Rule 4511 | A decision must be rebuildable, including the conversation, model version and prompt | [O3](../03-research/the-agent-in-operation.md), [V3](../03-research/consistency-and-change.md) |
| **Complaints** | FINRA Rules 4513 and 4530 | Complaints arrive as free text inside a conversation | [O3](../03-research/the-agent-in-operation.md); see [gaps](gaps-and-enforcement.md) |
| **Business continuity** | FINRA Rule 4370 | The agent depends on an external model service | [O2](../03-research/the-agent-in-operation.md) |
| **Third-party risk** | Interagency Guidance on Third-Party Relationships (2023); SR 26-2 principles on vendor models, by extension | The core model is rented and can change without notice | [T1, T2](../03-research/third-party-models.md), [V2](../03-research/consistency-and-change.md) |
| **Model risk management:** validation, change control, effective challenge | SR 26-2 (2026) principles, by extension: the guidance itself excludes generative and agentic AI | Every prompt edit and vendor update is treated as a model change; the evaluator is often a model too | [V2 to V4](../03-research/consistency-and-change.md), [M1 to M3](../03-research/measuring-honestly.md) |
| **Privacy** | Regulation S-P (2024 amendments) | Client data may flow to an outside model and back | [G1](../03-research/guardrails-under-attack.md) (privacy and leakage category); see [gaps](gaps-and-enforcement.md) |
| **Fair treatment** | Fiduciary duty | Answer quality and confidence can vary with how a client writes | [B3](../03-research/behaviour-when-the-user-changes.md), [K2](../03-research/honest-confidence.md) |

## AI-specific frameworks

The [NIST AI RMF and its Generative AI Profile (NIST AI 600-1)](../02-nist-ai-rmf/nist-ai-rmf.md)
do not add legal obligations. They give the structure used here to organise
the evidence: govern, map, measure, manage.

## A companion repository

Models used in investment advice and wealth management (risk profiling,
suitability, portfolio risk, conflicts in product choice) are covered in the
companion repository on investment and wealth management advisory validation.
This one covers language-model agents that talk to clients.
