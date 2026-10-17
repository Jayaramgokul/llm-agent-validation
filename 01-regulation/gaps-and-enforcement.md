# Governance gaps, and what regulators have acted on

> Public sources only; see [SOURCES.md](../SOURCES.md). Rules are summarised,
> not quoted; check their current status before relying on them.

## Where these gaps come from

Mapping the regulations against the whole life cycle of models used in
advice showed areas a standard model validation tends to miss, in three
pillars:

- suitability and client protection;
- conflicts of interest;
- governance and controls.

The first two are covered in the companion repository on investment and
wealth management advisory validation. The third, governance and controls,
is the least developed of the three, and it is where a language-model agent
changes most. It is set out here.

## Pillar C: governance and controls

| Area | Public rules | Why an LLM agent makes it harder | What to test | Tests here |
|---|---|---|---|---|
| **Third-party and model-vendor risk** | Interagency Guidance on Third-Party Relationships (2023); SR 26-2 principles on vendor models, by extension; FINRA Regulatory Notice 24-09 | The vendor can update the model and change the agent's behaviour without the firm changing anything | Due diligence, change-notice terms, regression on every vendor update, an exit plan | T1, T2, V2 |
| **Model inventory and documentation** | Firm policy (SR 26-2 excludes generative AI); NIST AI RMF | The "model" is a stack: vendor model, prompts, retrieval, guardrails, judge. Each part can change separately | Every component inventoried with owner, version, limits and monitoring | V3 |
| **Change management** | Firm policy (SR 26-2 excludes generative AI) | A one-line prompt edit can change advice for every client | Approval workflow; locked regression battery before release; version log | V2, V4 |
| **Complaints in a chat interface** | FINRA Rules 4513, 4530 and 3110 | Complaints arrive in natural language, mid-conversation, and are easy to miss | Recognition of complaint language, routing, retention of every interaction | O3 |
| **Business continuity** | FINRA Rule 4370; Compliance Rule 206(4)-7 | The agent depends on an external service that can fail mid-conversation | Safe failure, client messaging, fallback | O2 |
| **Privacy** | Regulation S-P (2024 amendments: incident response and notification) | Client data may be sent to an outside model, or leak through it | Data-flow map; leakage attacks; incident response covering AI-specific breaches | G1 (privacy and leakage category) |
| **Financial crime controls** | Bank Secrecy Act and AML programme rules; OFAC sanctions | A new advice channel must feed monitoring, not bypass it; the agent can be asked to help with abuse | Refusal of assistance with financial crime; every recommendation logged as an auditable event | G1 (financial crime category) |

## What regulators have acted on

| Action | What happened | What it means for validating an agent |
|---|---|---|
| **Delphia and Global Predictions (2024)**, SEC press release 2024-36 | Two advisers settled charges over false and misleading statements about their use of artificial intelligence; $400,000 in penalties in total. | What the firm, or the agent itself, says about the agent's capabilities must be true and substantiated ([B4](../03-research/behaviour-when-the-user-changes.md)). |
| **FINRA Regulatory Notice 24-09 (2024)** | FINRA reminded members that its rules are technology-neutral and apply to generative AI, highlighting supervision, communications, recordkeeping and vendor risk. | Every row of the table above is an existing obligation, not a future one. |
| **SEC examination priorities** (published annually) | Algorithmic advice and the use of AI have been recurring themes. | Examiners will ask for evidence of testing, so it needs to exist before the examination. |
