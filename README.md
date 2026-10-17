# LLM Agent Validation

![tests](https://github.com/Jayaramgokul/llm-agent-validation/actions/workflows/tests.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![licence](https://img.shields.io/badge/licence-MIT-green)

**How I approach the independent validation of language-model agents used
with clients in regulated financial services, with investment guidance as the
running example: how they change each existing obligation, where a standard
model review falls short, what the research says about testing those gaps,
and how each test is designed.**

> Draws on my experience validating AI and quantitative models in financial
> services. All examples use public sources and simulated data.

This is a validator's notebook, not software. The documents carry the
argument. The short Python scripts show individual methods working on
simulated evaluation outcomes. None of them calls a language model.

## The reasoning, in order

```
01 Regulation        How does an LLM agent change each existing obligation, and which governance gaps open up?
        │
        ▼
02 NIST AI RMF       Govern, map, measure, manage, plus the Generative AI Profile's risks
        │
        ▼
03 Research          What has the literature already learned about testing each behaviour?
        │
        ▼
04 Test design       Objective, client harm, data, method, pass criteria, NIST subcategory, regulatory hook
        │
        ▼
05 Illustrations     Each method on simulated outcomes, with its result explained in plain language
```

| Step | Read |
|---|---|
| 1. Obligations | [Regulatory map](01-regulation/regulatory-map.md): duty of care, communications, supervision, books and records, third-party risk, FINRA Regulatory Notice 24-09 |
| | [Governance gaps and enforcement](01-regulation/gaps-and-enforcement.md): vendor risk, change management, complaints in chat, continuity, privacy; the 2024 AI-washing cases |
| 2. Framework | [NIST AI RMF and the Generative AI Profile](02-nist-ai-rmf/nist-ai-rmf.md): which tests evidence which subcategory and which generative-AI risk |
| 3. Research | [Behaviour when the user changes](03-research/behaviour-when-the-user-changes.md): sycophancy, credential claims, sandbagging |
| | [Guardrails under attack](03-research/guardrails-under-attack.md): red-team failure rates with honest intervals |
| | [Measuring honestly](03-research/measuring-honestly.md): validating the LLM judge, the noise floor, multiple testing |
| | [Honest confidence](03-research/honest-confidence.md): calibration of confidence phrases, by group |
| | [Consistency and change](03-research/consistency-and-change.md): reproducibility, regression on every update |
| | [The agent in operation](03-research/the-agent-in-operation.md): faithful explanations, safe failure, retrieval in high dimensions |
| | [Third-party models](03-research/third-party-models.md): what to know about the rented model |
| 4. Method | [How the tests were derived](04-test-design/method.md) |
| 5. Catalogue | [All 25 tests](04-test-design/catalogue.md), each with its risk, method, pass criteria, NIST subcategory and regulatory hook |
| 6. Illustrations | [05-illustrations](05-illustrations/): 14 standalone scripts |
| Sources | [SOURCES.md](SOURCES.md) |

## A few things the illustrations show

| Test | On simulated outcomes |
|---|---|
| [B1 Sycophancy](05-illustrations/b1_sycophancy_pairs.py) | A stated bullish view moves a quarter of recommendations by more than 5 points; rerunning the same chat moves 2% |
| [G1 Red-team failure rate](05-illustrations/g1_red_team_failure_rate.py) | Zero failures in 18 financial-crime prompts still allows a true rate of 15%; proving below 1% takes 299 clean prompts |
| [M1 Validating the judge](05-illustrations/m1_validating_the_judge.py) | A judge with good agreement (kappa 0.79) still misses 11% of real failures and flips its verdict when answer order is swapped |
| [M2 Noise floor](05-illustrations/m2_noise_floor.py) | An unchanged model scores anywhere from 68% to 77%; a single-run "regression" of 3.7 points is noise |
| [K1 Calibration](05-illustrations/k1_calibration_of_confidence.py) | "Almost certain" outcomes happen 84% of the time |
| [V4 Safe updates](05-illustrations/v4_safe_updates.py) | A better-on-average update doubles failures for one group of clients in one situation |

![Calibration of confidence phrases](05-illustrations/output/k1_reliability.png)

## Run the illustrations

```bash
git clone https://github.com/Jayaramgokul/llm-agent-validation.git && cd llm-agent-validation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python 05-illustrations/g1_red_team_failure_rate.py   # any script; charts go to 05-illustrations/output/
python -m pytest tests/ -q                            # checks the shared statistics and runs every script
```

## Limitations

All outcomes are simulated, so the numbers illustrate methods, not any real
model or firm. Tolerances shown are examples; in a real validation they are
agreed with the model owner before testing. Regulations are summarised, not
quoted, and their current status should be checked before relying on them.

## Licence

MIT.
